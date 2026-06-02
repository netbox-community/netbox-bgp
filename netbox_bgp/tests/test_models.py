from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from tenancy.models import Tenant
from dcim.models import Site, Device, Manufacturer, DeviceRole, DeviceType
from ipam.models import IPAddress, ASN, RIR, Prefix

from netbox_bgp.models import (
    BGPSession, Community, CommunityList, CommunityListRule,
    RoutingPolicy, BGPPeerGroup, RoutingPolicyRule,
    ASPathList, ASPathListRule, PrefixList, PrefixListRule,
)
from netbox_bgp.choices import ActionChoices, IPAddressFamilyChoices


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


class CommunityListTestCase(TestCase):
    def setUp(self):
        self.communitylist = CommunityList.objects.create(
            name='community_list_1',
            description='test_community_list',
            comments='comment_cl1'
        )

    def test_create_community(self):
        self.assertTrue(isinstance(self.communitylist, CommunityList))
        self.assertEqual(self.communitylist.__str__(), self.communitylist.name)

    def test_unique_together(self):
        communitylist2 = CommunityList(
            name='community_list_1',
            description='test_community_list',
        )
        with self.assertRaises(IntegrityError):
            communitylist2.save()

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
            role=device_role,
            device_type=device_type
        )
        self.rir = RIR.objects.create(
            name="rir"
        )
        self.local_as = ASN.objects.create(
            asn=65001,
            rir=self.rir
        )
        self.remote_as = ASN.objects.create(
            asn=65002,
            rir=self.rir
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

    def test_label_with_name(self):
        self.assertEqual(self.session.label, 'session')

    def test_label_without_name(self):
        extra_ip = IPAddress.objects.create(address='1.1.1.3/32')
        nameless = BGPSession.objects.create(
            local_address=self.local_ip,
            remote_address=extra_ip,
            local_as=self.local_as,
            remote_as=self.remote_as,
            status='active',
        )
        self.assertIn(str(extra_ip), nameless.label)

    def test_policies(self):
        self.session.import_policies.add(self.routing_policy_in)
        self.session.export_policies.add(self.routing_policy_out)
        self.assertIn(self.routing_policy_in, self.session.import_policies.all())
        self.assertIn(self.routing_policy_out, self.session.export_policies.all())

    def test_unique_together(self):
        dup = BGPSession(
            device=self.device,
            local_address=self.local_ip,
            remote_address=self.remote_ip,
            local_as=self.local_as,
            remote_as=self.remote_as,
            status='active',
        )
        with self.assertRaises(IntegrityError):
            dup.save()


class ASPathListTestCase(TestCase):
    def setUp(self):
        self.apl = ASPathList.objects.create(name='apl1', description='test apl')

    def test_str(self):
        self.assertEqual(str(self.apl), 'apl1')

    def test_unique_together(self):
        dup = ASPathList(name='apl1', description='test apl')
        with self.assertRaises(IntegrityError):
            dup.save()


class ASPathListRuleTestCase(TestCase):
    def setUp(self):
        self.apl = ASPathList.objects.create(name='apl_rule_parent')
        self.rule = ASPathListRule.objects.create(
            aspath_list=self.apl,
            index=10,
            action=ActionChoices._choices[0][0],
            pattern='65000',
        )

    def test_str(self):
        self.assertEqual(
            str(self.rule),
            f'{self.apl}: {self.rule.action} {self.rule.pattern}',
        )

    def test_get_action_color(self):
        self.assertIsNotNone(self.rule.get_action_color())


class PrefixListTestCase(TestCase):
    def setUp(self):
        self.pl = PrefixList.objects.create(
            name='pl1',
            family=IPAddressFamilyChoices.FAMILY_4,
        )

    def test_str(self):
        self.assertEqual(str(self.pl), 'pl1')

    def test_unique_together(self):
        dup = PrefixList(name='pl1', description='', family=IPAddressFamilyChoices.FAMILY_4)
        with self.assertRaises(IntegrityError):
            dup.save()


class PrefixListRuleTestCase(TestCase):
    def setUp(self):
        self.pl = PrefixList.objects.create(
            name='pl_for_rules',
            family=IPAddressFamilyChoices.FAMILY_4,
        )
        self.prefix = Prefix.objects.create(prefix='10.0.0.0/8')

    def test_str(self):
        rule = PrefixListRule(prefix_list=self.pl, index=10, action='permit', prefix=self.prefix)
        self.assertEqual(str(rule), f'{self.pl}: Rule 10')

    def test_network_returns_prefix_fk(self):
        rule = PrefixListRule.objects.create(
            prefix_list=self.pl, index=10, action='permit', prefix=self.prefix
        )
        self.assertEqual(rule.network, self.prefix)

    def test_network_returns_prefix_custom(self):
        rule = PrefixListRule.objects.create(
            prefix_list=self.pl, index=20, action='permit', prefix_custom='0.0.0.0/0'
        )
        self.assertIsNotNone(rule.network)

    def test_get_action_color(self):
        rule = PrefixListRule.objects.create(
            prefix_list=self.pl, index=30, action='permit', prefix=self.prefix
        )
        self.assertIsNotNone(rule.get_action_color())

    def test_clean_rejects_both_prefix_fields_set(self):
        rule = PrefixListRule(
            prefix_list=self.pl,
            index=40,
            action='permit',
            prefix=self.prefix,
            prefix_custom='0.0.0.0/0',
        )
        with self.assertRaises(ValidationError):
            rule.clean()

    def test_clean_rejects_neither_prefix_field_set(self):
        rule = PrefixListRule(
            prefix_list=self.pl,
            index=50,
            action='permit',
        )
        with self.assertRaises(ValidationError):
            rule.clean()

    def test_clean_accepts_prefix_fk_only(self):
        rule = PrefixListRule(
            prefix_list=self.pl, index=60, action='permit', prefix=self.prefix
        )
        rule.clean()  # must not raise

    def test_clean_accepts_prefix_custom_only(self):
        rule = PrefixListRule(
            prefix_list=self.pl, index=70, action='permit', prefix_custom='0.0.0.0/0'
        )
        rule.clean()  # must not raise


class RoutingPolicyRuleTestCase(TestCase):
    def setUp(self):
        self.rp = RoutingPolicy.objects.create(name='rp_rule_test')
        self.rule = RoutingPolicyRule.objects.create(
            routing_policy=self.rp,
            index=10,
            action=ActionChoices._choices[0][0],
        )

    def test_str(self):
        self.assertEqual(str(self.rule), f'{self.rp}: Rule 10')

    def test_get_action_color(self):
        self.assertIsNotNone(self.rule.get_action_color())

    def test_set_statements_empty(self):
        self.assertEqual(self.rule.set_statements, {})

    def test_set_statements_with_actions(self):
        self.rule.set_actions = {'local-preference': 100}
        self.rule.save()
        self.assertEqual(self.rule.set_statements, {'local-preference': 100})

    def test_match_statements_empty(self):
        self.assertEqual(self.rule.match_statements, {})

    def test_match_statements_with_community(self):
        community = Community.objects.create(value='65000:100')
        self.rule.match_community.add(community)
        stmts = self.rule.match_statements
        self.assertIn('community', stmts)
        self.assertIn('65000:100', stmts['community'])

    def test_match_statements_with_prefix_list(self):
        pl = PrefixList.objects.create(name='pl_match', family=IPAddressFamilyChoices.FAMILY_4)
        self.rule.match_ip_address.add(pl)
        stmts = self.rule.match_statements
        self.assertIn('ip address', stmts)
        self.assertIn('pl_match', stmts['ip address'])

    def test_match_statements_with_aspath_list(self):
        apl = ASPathList.objects.create(name='apl_match')
        self.rule.match_aspath_list.add(apl)
        stmts = self.rule.match_statements
        self.assertIn('as-path', stmts)
        self.assertIn('apl_match', stmts['as-path'])


class CommunityListRuleTestCase(TestCase):
    def setUp(self):
        self.cl = CommunityList.objects.create(name='cl1')
        self.community = Community.objects.create(value='65001:100')
        self.rule = CommunityListRule.objects.create(
            community_list=self.cl,
            action=ActionChoices._choices[0][0],
            community=self.community,
        )

    def test_str(self):
        expected = f'{self.cl}: {self.rule.action} {self.community}'
        self.assertEqual(str(self.rule), expected)

    def test_get_action_color(self):
        self.assertIsNotNone(self.rule.get_action_color())


class CommunityScopeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        from dcim.models import Site
        from django.contrib.contenttypes.models import ContentType
        cls.site = Site.objects.create(name='Test Site')
        cls.community_with_scope = Community.objects.create(
            value='65000:100',
            scope_type=ContentType.objects.get_for_model(Site),
            scope_id=cls.site.pk
        )
        cls.community_without_scope = Community.objects.create(value='65000:101')

    def test_create_community_with_scope(self):
        from dcim.models import Site
        from django.contrib.contenttypes.models import ContentType
        community = Community(
            value='65000:102',
            scope_type=ContentType.objects.get_for_model(Site),
            scope_id=self.site.pk
        )
        community.full_clean()
        community.save()
        self.assertEqual(community.scope, self.site)

    def test_community_scope_type_validation(self):
        from dcim.models import Site
        from django.contrib.contenttypes.models import ContentType
        community = Community.objects.get(value='65000:100')
        self.assertEqual(community.scope_type, ContentType.objects.get_for_model(Site))
        self.assertEqual(community.scope, self.site)

    def test_community_scope_null(self):
        community = Community.objects.get(value='65000:101')
        self.assertIsNone(community.scope)
        self.assertIsNone(community.scope_type)
        self.assertIsNone(community.scope_id)

    def test_community_scope_str(self):
        community_with = Community.objects.get(value='65000:100')
        community_without = Community.objects.get(value='65000:101')
        self.assertEqual(str(community_with), '65000:100')
        self.assertEqual(str(community_without), '65000:101')

    def test_community_scope_change(self):
        from dcim.models import Site
        from django.contrib.contenttypes.models import ContentType
        site2 = Site.objects.create(name='Test Site 2')
        self.community_with_scope.scope_type = ContentType.objects.get_for_model(Site)
        self.community_with_scope.scope_id = site2.pk
        self.community_with_scope.save()
        self.assertEqual(self.community_with_scope.scope, site2)
