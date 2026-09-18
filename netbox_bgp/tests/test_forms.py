from http import HTTPStatus

from django.test import TestCase, override_settings

from ipam.models import IPAddress, ASN, RIR, VRF, Prefix

from netbox_bgp.choices import SessionStatusChoices
from netbox_bgp.forms import BGPSessionAddForm, CommunityBulkEditForm, CommunityForm
from netbox_bgp.models import Community


class TestCommunityFormCase(TestCase):
    def test_asn_invalid_letters(self):
        form = CommunityForm(
            data={
                'value': 'dsad',
                'status': 'active'
            }
        )
        self.assertEqual(
            form.errors['value'], ['Enter a valid value.']
        )

    def test_community_valid(self):
        form = CommunityForm(
            data={
                'value': '1234:5678',
                'status': 'active'
            }
        )
        self.assertEqual(
            form.errors.get('value'), None
        )


class CommunityBulkEditScopeTestCase(TestCase):
    """Scope handling in CommunityBulkEditForm — the scope field queryset must be
    populated from the selected scope_type so bulk edit validation succeeds."""

    @classmethod
    def setUpTestData(cls):
        from dcim.models import Site
        from django.contrib.contenttypes.models import ContentType

        cls.site = Site.objects.create(name='bulk-edit-site', slug='bulk-edit-site')
        cls.site_ct = ContentType.objects.get_for_model(Site)
        cls.community = Community.objects.create(value='65350:1')

    def test_scope_validates_with_scope_type(self):
        form = CommunityBulkEditForm(
            data={
                'pk': [self.community.pk],
                '_apply': '1',
                'scope_type': self.site_ct.pk,
                'scope': self.site.pk,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data.get('scope'), self.site)

    def test_scope_without_scope_type_is_left_untouched(self):
        form = CommunityBulkEditForm(
            data={'pk': [self.community.pk], '_apply': '1'}
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertNotIn('scope', form.changed_data)

    def test_scope_type_uses_bulk_edit_htmx_select(self):
        # BulkEditView.get() redirects to the return URL, so the HTMX scope-type
        # switch must POST and swap only #form_fields (mirrors ScopedBulkEditForm).
        widget = CommunityBulkEditForm()['scope_type'].field.widget
        attrs = widget.attrs
        self.assertEqual(attrs.get('hx-post'), '.')
        self.assertEqual(attrs.get('hx-select'), '#form_fields')
        self.assertEqual(attrs.get('hx-target'), '#form_fields')


class RemoteAddressStrictTestCase(TestCase):
    """Issue #289 — when remote_address_strict is enabled, BGPSessionAddForm
    must not auto-create an IPAddress for an unknown remote address."""

    @classmethod
    def setUpTestData(cls):
        rir = RIR.objects.create(name="rir_289")
        cls.local_as = ASN.objects.create(asn=65030, rir=rir)
        cls.remote_as = ASN.objects.create(asn=65031, rir=rir)
        cls.local_ip = IPAddress.objects.create(address="192.0.2.1/32")
        cls.existing_remote_ip = IPAddress.objects.create(address="192.0.2.2/32")
        # Two IPs with the same address in different VRFs — triggers MultipleObjectsReturned
        cls.vrf = VRF.objects.create(name="vrf_289")
        cls.dup_ip = IPAddress.objects.create(address="192.0.2.3/32")
        cls.dup_ip_vrf = IPAddress.objects.create(address="192.0.2.3/32", vrf=cls.vrf)

    def _form_data(self, remote_address):
        return {
            "local_as": self.local_as.pk,
            "remote_as": self.remote_as.pk,
            "local_address": self.local_ip.pk,
            "remote_address": remote_address,
            "status": SessionStatusChoices.STATUS_ACTIVE,
        }

    @override_settings(
        PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": False}}
    )
    def test_non_strict_auto_creates_remote_address(self):
        before = IPAddress.objects.count()
        form = BGPSessionAddForm(data=self._form_data("198.51.100.7/32"))
        self.assertTrue(form.is_valid())
        ip = form.cleaned_data.get("remote_address")
        self.assertIsInstance(ip, IPAddress)
        # Validation must not write: the IPAddress is created by save(), so that
        # a form which fails a later check leaves nothing behind.
        self.assertIsNone(ip.pk)
        self.assertEqual(IPAddress.objects.count(), before)

        session = form.save()
        self.assertEqual(IPAddress.objects.count(), before + 1)
        self.assertTrue(IPAddress.objects.filter(address="198.51.100.7/32").exists())
        self.assertEqual(str(session.remote_address.address), "198.51.100.7/32")
        self.assertIsNotNone(session.remote_address.pk)

    @override_settings(
        PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": False}}
    )
    def test_non_strict_reuses_existing_remote_address(self):
        before = IPAddress.objects.count()
        form = BGPSessionAddForm(data=self._form_data("192.0.2.2/32"))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("remote_address"), self.existing_remote_ip)
        self.assertEqual(IPAddress.objects.count(), before)

    @override_settings(
        PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": False}}
    )
    def test_non_strict_duplicate_address_picks_first_without_creating(self):
        before = IPAddress.objects.count()
        form = BGPSessionAddForm(data=self._form_data("192.0.2.3/32"))
        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.cleaned_data.get("remote_address"), IPAddress)
        self.assertEqual(IPAddress.objects.count(), before)

    @override_settings(
        PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": True}}
    )
    def test_strict_rejects_unknown_remote_address(self):
        before = IPAddress.objects.count()
        form = BGPSessionAddForm(data=self._form_data("198.51.100.8/32"))
        self.assertFalse(form.is_valid())
        self.assertIn("remote_address", form.errors)
        self.assertEqual(IPAddress.objects.count(), before)

    @override_settings(
        PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": True}}
    )
    def test_strict_accepts_existing_remote_address(self):
        form = BGPSessionAddForm(data=self._form_data(self.existing_remote_ip.pk))
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data.get("remote_address"), self.existing_remote_ip
        )


class RemotePrefixTestCase(TestCase):
    """Issue #282 — a session may nominate a prefix as its remote peer for
    dynamic peering. Exactly one of remote_address / remote_prefix is required."""

    @classmethod
    def setUpTestData(cls):
        rir = RIR.objects.create(name="rir_282")
        cls.local_as = ASN.objects.create(asn=65040, rir=rir)
        cls.remote_as = ASN.objects.create(asn=65041, rir=rir)
        cls.local_ip = IPAddress.objects.create(address="192.0.2.10/32")
        cls.remote_ip = IPAddress.objects.create(address="192.0.2.11/32")
        cls.prefix = Prefix.objects.create(prefix="203.0.113.0/24")

    def _form_data(self, **overrides):
        data = {
            "local_as": self.local_as.pk,
            "remote_as": self.remote_as.pk,
            "local_address": self.local_ip.pk,
            "status": SessionStatusChoices.STATUS_ACTIVE,
        }
        data.update(overrides)
        return data

    def test_prefix_only_is_valid(self):
        before = IPAddress.objects.count()
        form = BGPSessionAddForm(data=self._form_data(remote_prefix=self.prefix.pk))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data.get("remote_prefix"), self.prefix)
        self.assertIsNone(form.cleaned_data.get("remote_address"))
        # A blank remote_address must not auto-create an IPAddress
        self.assertEqual(IPAddress.objects.count(), before)

    def test_both_remote_address_and_prefix_rejected(self):
        form = BGPSessionAddForm(
            data=self._form_data(
                remote_address="192.0.2.11/32", remote_prefix=self.prefix.pk
            )
        )
        self.assertFalse(form.is_valid())
        self.assertIn("remote_prefix", form.errors)

    def test_rejected_form_does_not_leave_orphan_remote_address(self):
        """An unknown remote_address combined with a remote_prefix is rejected by
        Model.clean(). The address must not have been created along the way."""
        before = IPAddress.objects.count()
        form = BGPSessionAddForm(
            data=self._form_data(
                remote_address="198.51.100.99/32", remote_prefix=self.prefix.pk
            )
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(IPAddress.objects.count(), before)
        self.assertFalse(
            IPAddress.objects.filter(address="198.51.100.99/32").exists()
        )

    def test_neither_remote_address_nor_prefix_rejected(self):
        form = BGPSessionAddForm(data=self._form_data())
        self.assertFalse(form.is_valid())
        self.assertIn("remote_address", form.errors)
