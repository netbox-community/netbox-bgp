from http import HTTPStatus

from django.test import TestCase, override_settings

from ipam.models import IPAddress, ASN, RIR

from netbox_bgp.choices import SessionStatusChoices
from netbox_bgp.forms import BGPSessionAddForm, CommunityForm


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
        form.is_valid()
        self.assertIsInstance(form.cleaned_data.get("remote_address"), IPAddress)
        self.assertTrue(IPAddress.objects.filter(address="198.51.100.7/32").exists())
        self.assertEqual(IPAddress.objects.count(), before + 1)

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
        form.is_valid()
        self.assertEqual(
            form.cleaned_data.get("remote_address"), self.existing_remote_ip
        )
