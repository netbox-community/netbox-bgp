from django.test import TestCase, override_settings
from ipam.models import IPAddress, ASN, RIR
from dcim.models import Site, Device, Manufacturer, DeviceRole, DeviceType
from netbox_bgp.forms import CommunityForm, BGPSessionAddForm
from netbox_bgp.models import SessionStatusChoices


class TestCommunityFormCase(TestCase):
    def test_asn_invalid_letters(self):
        form = CommunityForm(data={"value": "dsad", "status": "active"})
        self.assertEqual(form.errors["value"], ["Enter a valid value."])

    def test_community_valid(self):
        form = CommunityForm(data={"value": "1234:5678", "status": "active"})
        self.assertEqual(form.errors.get("value"), None)


class BGPSessionAddFormTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.create(name="test-site", slug="test-site")
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", slug="test-manufacturer"
        )
        self.device_role = DeviceRole.objects.create(name="Test Role", slug="test-role")
        self.device_type = DeviceType.objects.create(
            manufacturer=self.manufacturer, model="Test Device", slug="test-device"
        )
        self.device = Device.objects.create(
            name="test-device",
            site=self.site,
            device_type=self.device_type,
            role=self.device_role,
        )

        # Create existing IP addresses
        self.local_ip = IPAddress.objects.create(address="1.1.1.1/32")
        self.existing_remote_ip = IPAddress.objects.create(address="2.2.2.2/32")

        # Create ASNs
        self.rir = RIR.objects.create(name="Test RIR", slug="test-rir")
        self.local_as = ASN.objects.create(asn=65001, rir=self.rir)
        self.remote_as = ASN.objects.create(asn=65002, rir=self.rir)

    @override_settings(PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": False}})
    def test_non_strict_mode_allows_creation(self):
        """Test that non-strict mode allows IP creation"""
        form_data = {
            "name": "test-session",
            "status": SessionStatusChoices.STATUS_ACTIVE,
            "local_address": self.local_ip.id,
            "remote_address": "3.3.3.3/32",  # Non-existent IP
            "local_as": self.local_as.id,
            "remote_as": self.remote_as.id,
            "device": self.device.id,
        }
        form = BGPSessionAddForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Verify IP was created
        self.assertTrue(IPAddress.objects.filter(address="3.3.3.3/32").exists())

    @override_settings(PLUGINS_CONFIG={}) # Default strict mode
    def test_non_strict_mode_uses_existing_ip(self):
        """Test that non-strict mode can use existing IPs"""
        form_data = {
            "name": "test-session",
            "status": SessionStatusChoices.STATUS_ACTIVE,
            "local_address": self.local_ip.id,
            "remote_address": "2.2.2.2/32",  # Existing IP
            "local_as": self.local_as.id,
            "remote_as": self.remote_as.id,
            "device": self.device.id,
        }
        form = BGPSessionAddForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["remote_address"].id, self.existing_remote_ip.id
        )

    @override_settings(PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": True}})
    def test_strict_mode_requires_existing_ip(self):
        """Test that strict mode requires existing IP"""
        form_data = {
            "name": "test-session",
            "local_address": self.local_ip.id,
            "remote_address": self.existing_remote_ip.id,  # Use existing IP ID
            "local_as": self.local_as.id,
            "remote_as": self.remote_as.id,
            "device": self.device.id,
            "status": SessionStatusChoices.STATUS_ACTIVE,
        }
        form = BGPSessionAddForm(data=form_data)
        self.assertTrue(form.is_valid())

    @override_settings(PLUGINS_CONFIG={"netbox_bgp": {"remote_address_strict": True}})
    def test_strict_mode_rejects_nonexistent_ip(self):
        """Test that strict mode rejects non-existent IPs"""
        form_data = {
            "name": "test-session",
            "local_address": self.local_ip.id,
            "status": SessionStatusChoices.STATUS_ACTIVE,
            "remote_address": "4.4.4.4/32",  # Non-existent IP
            "local_as": self.local_as.id,
            "remote_as": self.remote_as.id,
            "device": self.device.id,
        }
        form = BGPSessionAddForm(data=form_data)
        # Form should be invalid because IP doesn't exist
        self.assertFalse(form.is_valid())
        self.assertIn("remote_address", form.errors)

    @override_settings(PLUGINS_CONFIG={"netbox_bgp": {}}) # Empty config to ensure default behavior
    def test_default_mode_is_non_strict(self):
        """Test that default mode is non-strict (backward compatibility)"""
        form_data = {
            "name": "test-session",
            "status": SessionStatusChoices.STATUS_ACTIVE,
            "local_address": self.local_ip.id,
            "remote_address": "5.5.5.5/32",  # Non-existent IP
            "local_as": self.local_as.id,
            "remote_as": self.remote_as.id,
            "device": self.device.id,
        }
        form = BGPSessionAddForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Verify IP was created (non-strict behavior)
        self.assertTrue(IPAddress.objects.filter(address="5.5.5.5/32").exists())
