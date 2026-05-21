from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress, ASN, RIR

from netbox_bgp.filtersets import (
    ASPathListFilterSet,
    BGPPeerGroupFilterSet,
    BGPSessionFilterSet,
    CommunityFilterSet,
    CommunityListFilterSet,
    PrefixListFilterSet,
    RoutingPolicyFilterSet,
)
from netbox_bgp.models import (
    ASPathList,
    BGPPeerGroup,
    BGPSession,
    Community,
    CommunityList,
    PrefixList,
    RoutingPolicy,
)
from netbox_bgp.choices import IPAddressFamilyChoices


class ASPathListFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ASPathList.objects.bulk_create([
            ASPathList(name='apl_fs_1', description='first one'),
            ASPathList(name='apl_fs_2', description='second one'),
            ASPathList(name='apl_fs_3', description='third one'),
        ])

    def _qs(self):
        return ASPathList.objects.filter(name__startswith='apl_fs_')

    def test_search_by_name(self):
        fs = ASPathListFilterSet({'q': 'apl_fs_1'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)
        self.assertEqual(fs.qs.first().name, 'apl_fs_1')

    def test_search_by_description(self):
        fs = ASPathListFilterSet({'q': 'second one'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_empty_returns_all(self):
        fs = ASPathListFilterSet({'q': ''}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_name(self):
        # name uses MultiValueCharFilter (list → __in lookup)
        fs = ASPathListFilterSet({'name': ['apl_fs_2']}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)
        self.assertEqual(fs.qs.first().name, 'apl_fs_2')

    def test_filter_by_name_no_match(self):
        fs = ASPathListFilterSet({'name': ['does_not_exist']}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 0)


class CommunityFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Community.objects.bulk_create([
            Community(value='65300:1', description='first community', status='active'),
            Community(value='65300:2', description='second community', status='active'),
            Community(value='65300:3', description='third community', status='deprecated'),
        ])

    def _qs(self):
        return Community.objects.filter(value__startswith='65300:')

    def test_search_by_value(self):
        fs = CommunityFilterSet({'q': '65300:1'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_by_description(self):
        fs = CommunityFilterSet({'q': 'second community'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_whitespace_returns_all(self):
        fs = CommunityFilterSet({'q': '   '}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_status_deprecated(self):
        # status uses ChoiceFilter (single string value)
        fs = CommunityFilterSet({'status': 'deprecated'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_status_active(self):
        fs = CommunityFilterSet({'status': 'active'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 2)


class CommunityListFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CommunityList.objects.bulk_create([
            CommunityList(name='clf_1', description='alpha list'),
            CommunityList(name='clf_2', description='beta list'),
            CommunityList(name='clf_3', description='gamma list'),
        ])

    def _qs(self):
        return CommunityList.objects.filter(name__startswith='clf_')

    def test_search_by_name(self):
        fs = CommunityListFilterSet({'q': 'clf_1'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_by_description(self):
        fs = CommunityListFilterSet({'q': 'beta list'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_empty_returns_all(self):
        fs = CommunityListFilterSet({'q': ''}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_name(self):
        fs = CommunityListFilterSet({'name': ['clf_3']}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)


class RoutingPolicyFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        RoutingPolicy.objects.bulk_create([
            RoutingPolicy(name='rpf_1', description='alpha policy'),
            RoutingPolicy(name='rpf_2', description='beta policy'),
            RoutingPolicy(name='rpf_3', description='gamma policy'),
        ])

    def _qs(self):
        return RoutingPolicy.objects.filter(name__startswith='rpf_')

    def test_search_by_name(self):
        fs = RoutingPolicyFilterSet({'q': 'rpf_1'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_by_description(self):
        fs = RoutingPolicyFilterSet({'q': 'beta policy'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_empty_returns_all(self):
        fs = RoutingPolicyFilterSet({'q': ''}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_name(self):
        fs = RoutingPolicyFilterSet({'name': ['rpf_2']}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)


class BGPPeerGroupFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        BGPPeerGroup.objects.bulk_create([
            BGPPeerGroup(name='pgf_1', description='alpha group'),
            BGPPeerGroup(name='pgf_2', description='beta group'),
            BGPPeerGroup(name='pgf_3', description='gamma group'),
        ])

    def _qs(self):
        return BGPPeerGroup.objects.filter(name__startswith='pgf_')

    def test_search_by_name(self):
        fs = BGPPeerGroupFilterSet({'q': 'pgf_1'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_by_description(self):
        fs = BGPPeerGroupFilterSet({'q': 'beta group'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_empty_returns_all(self):
        fs = BGPPeerGroupFilterSet({'q': ''}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_name(self):
        fs = BGPPeerGroupFilterSet({'name': ['pgf_3']}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)


class PrefixListFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        PrefixList.objects.bulk_create([
            PrefixList(name='plf_1', family=IPAddressFamilyChoices.FAMILY_4, description='ipv4 list'),
            PrefixList(name='plf_2', family=IPAddressFamilyChoices.FAMILY_6, description='ipv6 list'),
            PrefixList(name='plf_3', family=IPAddressFamilyChoices.FAMILY_4, description='another ipv4'),
        ])

    def _qs(self):
        return PrefixList.objects.filter(name__startswith='plf_')

    def test_search_by_name(self):
        fs = PrefixListFilterSet({'q': 'plf_1'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_by_description(self):
        fs = PrefixListFilterSet({'q': 'ipv6 list'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_empty_returns_all(self):
        fs = PrefixListFilterSet({'q': ''}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_family_ipv6(self):
        # family uses ChoiceFilter (single string value)
        fs = PrefixListFilterSet({'family': IPAddressFamilyChoices.FAMILY_6}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_family_ipv4(self):
        fs = PrefixListFilterSet({'family': IPAddressFamilyChoices.FAMILY_4}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 2)


class BGPSessionFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        mfr = Manufacturer.objects.create(name='fsf_mfr')
        dt = DeviceType.objects.create(manufacturer=mfr, model='fsf_dt')
        role = DeviceRole.objects.create(name='fsf_role')
        site = Site.objects.create(name='fsf_site')
        cls.device = Device.objects.create(
            name='fsf_device', site=site, role=role, device_type=dt,
        )
        rir = RIR.objects.create(name='fsf_rir')
        cls.local_as = ASN.objects.create(asn=65400, rir=rir)
        cls.remote_as = ASN.objects.create(asn=65401, rir=rir)

        cls.sessions = []
        for i in range(3):
            local_ip = IPAddress.objects.create(address=f'10.10.0.{i + 1}/32')
            remote_ip = IPAddress.objects.create(address=f'10.10.1.{i + 1}/32')
            cls.sessions.append(
                BGPSession.objects.create(
                    name=f'fsf_session_{i}',
                    device=cls.device,
                    local_address=local_ip,
                    remote_address=remote_ip,
                    local_as=cls.local_as,
                    remote_as=cls.remote_as,
                    status='active',
                )
            )

    def _qs(self):
        return BGPSession.objects.filter(name__startswith='fsf_session_')

    def test_filter_by_status(self):
        fs = BGPSessionFilterSet({'status': ['active']}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_device_name(self):
        fs = BGPSessionFilterSet({'device': ['fsf_device']}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_device_id(self):
        fs = BGPSessionFilterSet({'device_id': [self.device.pk]}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_local_as(self):
        fs = BGPSessionFilterSet({'local_as': [65400]}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_remote_as(self):
        fs = BGPSessionFilterSet({'remote_as': [65401]}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_search_by_remote_ip_cidr(self):
        fs = BGPSessionFilterSet({'by_remote_address': '10.10.1.1/32'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_by_remote_ip_invalid(self):
        fs = BGPSessionFilterSet({'by_remote_address': 'not-an-ip'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 0)

    def test_search_by_remote_ip_empty(self):
        fs = BGPSessionFilterSet({'by_remote_address': '  '}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)

    def test_search_by_local_ip_cidr(self):
        fs = BGPSessionFilterSet({'by_local_address': '10.10.0.1/32'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 1)

    def test_search_by_local_ip_invalid(self):
        fs = BGPSessionFilterSet({'by_local_address': 'invalid'}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 0)

    def test_search_by_local_ip_empty(self):
        fs = BGPSessionFilterSet({'by_local_address': ''}, queryset=self._qs())
        self.assertEqual(fs.qs.count(), 3)
