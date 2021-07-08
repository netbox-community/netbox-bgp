from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from tenancy.models import Tenant
from dcim.models import Site, Device, Manufacturer, DeviceRole, DeviceType
from ipam.models import IPAddress

from netbox_bgp.models import ASN, BGPSession, Community, RoutingPolicy, BGPPeerGroup


class ASNTestCase(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='tenant')
        self.asn = ASN.objects.create(
            number=65001,
            description='test_asn'
        )

    def test_create_asn(self):
        self.assertTrue(isinstance(self.asn, ASN))
        self.assertEqual(self.asn.__str__(), str(self.asn.number))

    def test_invalid_asn0(self):
        asn = ASN(number=0)
        self.assertRaises(ValidationError, asn.full_clean)

    def test_invalid_asndohuya(self):
        asn = ASN(number=4294967295)
        self.assertRaises(ValidationError, asn.full_clean)

    def test_uniqueconstraint_asn(self):
        asn = ASN(number=65001)
        with self.assertRaises(IntegrityError):
            asn.save()

    def test_uniqueconstraint_asn2(self):
        asn = ASN.objects.create(number=65001, tenant=self.tenant)
        self.assertEqual(str(asn), '65001')
        # todo cre another 65001 tenant=self.tenant


class RoutingPolicyTestCase(TestCase):
    def setUp(self):
        rp_name = 'test_policy'
        self.rp = RoutingPolicy.objects.create(
            name=rp_name,
            description=rp_name
        )

    def test_create_routing_policy(self):
        self.assertTrue(isinstance(self.rp, RoutingPolicy))
        self.assertEqual(self.rp.__str__(), self.rp.name)

    def test_unique_together(self):
        rp = RoutingPolicy(name=self.rp.name, description=self.rp.description)
        with self.assertRaises(IntegrityError):
            rp.save()


class BGPPeerGroupTestCase(TestCase):
    def setUp(self):
        self.in_policy1 = RoutingPolicy.objects.create(
            name='in_policy_1'
        )
        self.in_policy2 = RoutingPolicy.objects.create(
            name='in_policy_2'
        )
        self.out_policy1 = RoutingPolicy.objects.create(
            name='out_policy_1'
        )
        self.out_policy2 = RoutingPolicy.objects.create(
            name='out_policy_2'
        )
        self.peer_group = BGPPeerGroup.objects.create(
            name='peer_group',
            description='peer_group'
        )

    def test_create_peer_group(self):
        self.assertTrue(isinstance(self.peer_group, BGPPeerGroup))
        self.assertEqual(self.peer_group.__str__(), self.peer_group.name)

    def test_peer_group_polciy_realtions(self):
        peer_group = BGPPeerGroup.objects.create(
            name='group1',
        )
        peer_group.import_policies.add(self.in_policy1)
        peer_group.import_policies.add(self.in_policy2)
        peer_group.export_policies.add(self.out_policy1)
        peer_group.export_policies.add(self.out_policy2)
        self.assertEqual(
            peer_group.import_policies.get(
                pk=self.in_policy1.pk
            ),
            self.in_policy1
        )
        self.assertEqual(
            peer_group.import_policies.get(
                pk=self.in_policy2.pk
            ),
            self.in_policy2
        )
        self.assertEqual(
            peer_group.export_policies.get(
                pk=self.out_policy1.pk
            ),
            self.out_policy1
        )
        self.assertEqual(
            peer_group.export_policies.get(
                pk=self.out_policy2.pk
            ),
            self.out_policy2
        )

    def test_unique_together(self):
        peer_group = BGPPeerGroup(
            name='peer_group',
            description='peer_group'
        )
        with self.assertRaises(IntegrityError):
            peer_group.save()

    def test_ununique_together(self):
        peer_group1 = BGPPeerGroup(
            name='peer_group1',
            description='peer_group'
        )
        peer_group1.save()


class CommunityTestCase(TestCase):
    def setUp(self):
        self.community = Community.objects.create(
            value='65001:65001',
            description='test_community'
        )

    def test_create_community(self):
        self.assertTrue(isinstance(self.community, Community))
        self.assertEqual(self.community.__str__(), self.community.value)

    def test_invalid_community(self):
        community = Community(value=0)
        self.assertRaises(ValidationError, community.full_clean)


class BGPSessionTestCase(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name='manufacturer'
        )
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer,
            model='device type'
        )
        device_role = DeviceRole.objects.create(
            name='device role'
        )
        self.site = Site.objects.create(
            name='site'
        )
        self.tenant = Tenant.objects.create(
            name='tenant'
        )
        self.device = Device.objects.create(
            name='device',
            site=self.site,
            device_role=device_role,
            device_type=device_type
        )
        self.local_as = ASN.objects.create(
            number=65001,
        )
        self.remote_as = ASN.objects.create(
            number=65002,
        )
        self.peer_group = BGPPeerGroup.objects.create(
            name='peer_group'
        )
        self.routing_policy_in = RoutingPolicy.objects.create(
            name='policy_in'
        )
        self.routing_policy_out = RoutingPolicy.objects.create(
            name='policy_out'
        )
        self.local_ip = IPAddress.objects.create(
            address='1.1.1.1/32'
        )
        self.remote_ip = IPAddress.objects.create(
            address='1.1.1.2/32'
        )
        self.session = BGPSession.objects.create(
            name='session',
            site=self.site,
            tenant=self.tenant,
            device=self.device,
            local_address=self.local_ip,
            remote_address=self.remote_ip,
            local_as=self.local_as,
            remote_as=self.remote_as,
            status='active',
            peer_group=self.peer_group,
        )

    def test_create_session(self):
        self.assertTrue(isinstance(self.session, BGPSession))
        self.assertEqual(self.session.__str__(), f'{self.session.device}:{self.session.name}')

    def test_policies(self):
        pass

    def test_unique_together(self):
        pass
