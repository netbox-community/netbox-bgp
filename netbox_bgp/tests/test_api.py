import json

from django.urls import reverse
from utilities.testing import APITestCase, APIViewTestCases

from tenancy.models import Tenant
from dcim.models import Site, DeviceRole, DeviceType, Manufacturer, Device, Interface
from ipam.models import IPAddress, ASN, RIR, Prefix

from netbox_bgp.models import (
    Community,
    CommunityList,
    CommunityListRule,
    BGPPeerGroup,
    BGPSession,
    RoutingPolicy,
    RoutingPolicyRule,
    PrefixList,
    PrefixListRule,
)

from netbox_bgp.choices import (
    SessionStatusChoices,
    IPAddressFamilyChoices,
    ActionChoices,
)


class CommunityAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = Community
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id", "url", "value"]
    graphql_base_name = "netbox_bgp_community"

    create_data = [
        {"value": "65001:65000"},
        {"value": "65002:65001"},
        {"value": "65003:65002"},
    ]

    bulk_update_data = {
        "description": "Test Community desc",
    }

    @classmethod
    def setUpTestData(cls):
        communities = (
            Community(value="65000:65000"),
            Community(value="65000:65001"),
            Community(value="65000:65002"),
        )
        Community.objects.bulk_create(communities)


class CommunityListAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = CommunityList
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id", "name", "url"]
    graphql_base_name = "netbox_bgp_communitylist"

    create_data = [
        {"name": "CL1", "description": "cl1_api"},
        {"name": "CL2", "description": "cl2_api"},
        {"name": "CL3", "description": "cl3_api"},
    ]

    bulk_update_data = {
        "description": "Test Community List desc",
    }
    user_permissions = [
        "netbox_bgp.view_community",
    ]

    @classmethod
    def setUpTestData(cls):
        communitylists = (
            CommunityList(name="CL4", description="cl4"),
            CommunityList(name="CL5", description="cl5"),
            CommunityList(name="CL6", description="cl6"),
        )
        CommunityList.objects.bulk_create(communitylists)


class CommunityListRuleAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = CommunityListRule
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id"]
    graphql_base_name = "netbox_bgp_communitylist_rule"

    bulk_update_data = {
        "description": "Test Community List rules desc",
        "action": "deny",
    }

    user_permissions = [
        "netbox_bgp.view_communitylist",
        "netbox_bgp.view_community",
    ]


    @classmethod
    def setUpTestData(cls):
        com_list1 = CommunityList.objects.create(
            name="community list 1", description="community list 1"
        )
        com_list2 = CommunityList.objects.create(
            name="community list 2", description="community list 2"
        )
        com1 = Community.objects.create(value="65001:65004", description="community1")
        com2 = Community.objects.create(value="65002:65005", description="community2")
        com3 = Community.objects.create(value="65003:65006", description="community3")

        communitylistrules = (
            CommunityListRule(
                community_list=com_list1,
                community=com1,
                action=ActionChoices._choices[0][0],
                description="rule1",
            ),
            CommunityListRule(
                community_list=com_list1,
                community=com2,
                action=ActionChoices._choices[0][0],
                description="rule2",
            ),
            CommunityListRule(
                community_list=com_list1,
                community=com3,
                action=ActionChoices._choices[0][1],
                description="rule3",
            ),
        )
        CommunityListRule.objects.bulk_create(communitylistrules)

        cls.create_data = [
            {
                "community_list": com_list2.id,
                "description": "rule4",
                "community": com1.id,
                "action": "permit",
                "comments": "rule4",
            },
            {
                "community_list": com_list2.id,
                "description": "rule5",
                "community": com2.id,
                "action": "permit",
                "comments": "rule5",
            },
            {
                "community_list": com_list2.id,
                "description": "rule6",
                "community": com3.id,
                "action": "deny",
                "comments": "rule6",
            },
        ]


class BGPPeerGroupAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = BGPPeerGroup
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id", "name", "url"]
    graphql_base_name = "netbox_bgp_peer_group"

    create_data = [
        {
            "name": "test_peer_group",
            "description": "peer_group_desc",
            "comments": "peer_group_comment1",
        },
        {
            "name": "test_peer_group2",
            "description": "peer_group_desc2",
            "comments": "peer_group_comment2",
        },
        {
            "name": "test_peer_group3",
            "description": "peer_group_desc3",
            "comments": "peer_group_comment3",
        },
    ]

    bulk_update_data = {
        "description": "Test Community desc",
    }

    @classmethod
    def setUpTestData(cls):
        peer_groups = (
            BGPPeerGroup(
                name="peer group 1", description="peer group 1", comments="peer group 1"
            ),
            BGPPeerGroup(
                name="peer group 2", description="peer group 2", comments="peer group 2"
            ),
            BGPPeerGroup(
                name="peer group 3", description="peer group 3", comments="peer group 3"
            ),
        )
        BGPPeerGroup.objects.bulk_create(peer_groups)


class BGPSessionAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = BGPSession
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id", "name", "url"]
    graphql_base_name = "netbox_bgp_session"

    bulk_update_data = {
        "description": "Test BGP session desc",
    }
    user_permissions = [
        "ipam.view_ipaddress",
        "ipam.view_asn"
    ]


    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name="test", slug="test")
        manufacturer = Manufacturer.objects.create(name="Juniper", slug="juniper")
        device_role = DeviceRole.objects.create(name="Firewall", slug="firewall")
        device_type = DeviceType.objects.create(
            slug="srx3600", model="SRX3600", manufacturer=manufacturer
        )
        device = Device.objects.create(
            device_type=device_type, name="device1", role=device_role, site=site
        )
        device2 = Device.objects.create(
            device_type=device_type, name="device2", role=device_role, site=site
        )
        intf = Interface.objects.create(name="test_intf1", device=device)
        intf2 = Interface.objects.create(name="test_intf2", device=device)
        intf3 = Interface.objects.create(name="test_intf3", device=device)
        local_ip = IPAddress.objects.create(address="1.1.1.1/32")
        remote_ip1 = IPAddress.objects.create(address="2.2.2.2/32")
        remote_ip2 = IPAddress.objects.create(address="3.3.3.3/32")
        remote_ip3 = IPAddress.objects.create(address="4.4.4.4/32")
        intf.ip_addresses.add(local_ip)
        rir = RIR.objects.create(name="rir")
        local_as = ASN.objects.create(asn=65002, rir=rir, description="local_as")
        remote_as = ASN.objects.create(asn=65003, rir=rir, description="remote_as")
        peer_group = BGPPeerGroup.objects.create(
            name="peer_group", description="peer_group_description"
        )
        rp = RoutingPolicy.objects.create(
            name="rp1", description="test_rp", comments="comments_routing_policy"
        )
        pl1 = PrefixList.objects.create(
            name="pl1",
            description="test_pl",
            family=IPAddressFamilyChoices.FAMILY_4,
            comments="comments_pl",
        )

        sessions = (
            BGPSession(
                name="Session1",
                description="Session1",
                comments="Session1",
                local_as=local_as,
                remote_as=remote_as,
                local_address=local_ip,
                remote_address=remote_ip1,
                peer_group=peer_group,
                status=SessionStatusChoices.STATUS_ACTIVE,
            ),
            BGPSession(
                name="Session2",
                description="Session2",
                comments="Session2",
                local_as=local_as,
                remote_as=remote_as,
                local_address=local_ip,
                remote_address=remote_ip1,
                peer_group=peer_group,
                status=SessionStatusChoices.STATUS_ACTIVE,
            ),
            BGPSession(
                name="Session3",
                description="Session3",
                comments="Session3",
                local_as=local_as,
                remote_as=remote_as,
                local_address=local_ip,
                remote_address=remote_ip1,
                peer_group=peer_group,
                status=SessionStatusChoices.STATUS_ACTIVE,
                prefix_list_in=pl1,
            ),
        )
        BGPSession.objects.bulk_create(sessions)

        # sessions[0].import_policies.add(rp)

        cls.create_data = [
            {
                "name": "test_session1",
                "description": "test_session1",
                "comments": "test_session1",
                "local_as": local_as.id,
                "remote_as": remote_as.id,
                "device": device2.id,
                "local_address": local_ip.id,
                "remote_address": remote_ip1.id,
                "export_policies": [rp.id],
            },
            {
                "name": "test_session2",
                "description": "test_session2",
                "comments": "test_session2",
                "local_as": local_as.id,
                "remote_as": remote_as.id,
                "device": device2.id,
                "local_address": local_ip.id,
                "remote_address": remote_ip2.id,
                "import_policies": [rp.id],
            },
            {
                "name": "test_session3",
                "description": "test_session3",
                "comments": "test_session3",
                "local_as": local_as.id,
                "remote_as": remote_as.id,
                "device": device2.id,
                "local_address": local_ip.id,
                "remote_address": remote_ip3.id,
                "prefix_list_in": pl1.id,
            },
        ]


class RoutingPolicyAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = RoutingPolicy
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id", "name", "url"]
    graphql_base_name = "netbox_bgp_routing_policy"

    create_data = [
        {
            "name": "test_routing_policy",
            "description": "routing_policy_desc",
            "comments": "routing_policy_comment1",
        },
        {
            "name": "test_routing_policy2",
            "description": "routing_policy_desc2",
            "comments": "routing_policy_comment2",
        },
        {
            "name": "test_routing_policy3",
            "description": "routing_policy_desc3",
            "comments": "routing_policy_comment3",
        },
    ]

    bulk_update_data = {
        "description": "Test Routing policy desc",
    }

    @classmethod
    def setUpTestData(cls):
        routing_policies = (
            RoutingPolicy(
                name="Route-map 1", description="Route-map 1", comments="Route-map 1"
            ),
            RoutingPolicy(
                name="Route-map 2", description="Route-map 2", comments="Route-map 2"
            ),
            RoutingPolicy(
                name="Route-map 3", description="Route-map 3", comments="Route-map 3"
            ),
        )
        RoutingPolicy.objects.bulk_create(routing_policies)


class RoutingPolicyRuleAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = RoutingPolicyRule
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id"]
    graphql_base_name = "netbox_bgp_routing_policy_rule"

    bulk_update_data = {
        "description": "Test Routing policy rules desc",
        "action": "deny",
    }

    user_permissions = [
        "netbox_bgp.view_routingpolicy",
    ]


    @classmethod
    def setUpTestData(cls):
        rp1 = RoutingPolicy.objects.create(
            name="rp1", description="test_rp1", comments="comments_routing_policy1"
        )
        rp2 = RoutingPolicy.objects.create(
            name="rp2", description="test_rp2", comments="comments_routing_policy2"
        )
        pl1 = PrefixList.objects.create(
            name="pl1", description="test_pl", family=IPAddressFamilyChoices.FAMILY_4
        )
        pl2 = PrefixList.objects.create(
            name="pl1", description="test_pl", family=IPAddressFamilyChoices.FAMILY_6
        )
        com1 = Community.objects.create(value="65000:65000")
        com_list1 = CommunityList.objects.create(
            name="community list 1", description="community list 1"
        )

        routing_policies_rules = (
            RoutingPolicyRule(
                routing_policy=rp1,
                index=10,
                action=ActionChoices._choices[0][0],
                description="Rule1",
            ),
            RoutingPolicyRule(
                routing_policy=rp1,
                index=20,
                action=ActionChoices._choices[0][0],
                description="Rule2",
            ),
            RoutingPolicyRule(
                routing_policy=rp1,
                index=30,
                action=ActionChoices._choices[0][1],
                description="Rule3",
            ),
        )
        RoutingPolicyRule.objects.bulk_create(routing_policies_rules)

        cls.create_data = [
            {
                "routing_policy": rp2.id,
                "description": "rule4",
                "index": 10,
                "action": "permit",
                "comments": "rule4",
                "match_ip_address": [pl1.id],
            },
            {
                "routing_policy": rp2.id,
                "description": "rule5",
                "index": 20,
                "action": "permit",
                "comments": "rule5",
                "match_ipv6_address": [pl2.id],
                "set_actions": "{'set': 'origin incomplete'",
            },
            {
                "routing_policy": rp2.id,
                "description": "rule6",
                "index": 30,
                "action": "deny",
                "comments": "rule6",
                "match_community": [com1.id],
            },
            {
                "routing_policy": rp2.id,
                "description": "rule7",
                "index": 40,
                "action": "deny",
                "comments": "rule6",
                "match_community_list": [com_list1.id],
            },
        ]


class PrefixListAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = PrefixList
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id", "name", "url"]
    graphql_base_name = "netbox_bgp_prefixlist"

    create_data = [
        {
            "name": "test_prefix_list",
            "description": "prefix_list_desc",
            "comments": "prefix_list_comment1",
            "family": "ipv4",
        },
        {
            "name": "test_prefix_list2",
            "description": "prefix_list_desc2",
            "comments": "prefix_list_comment2",
            "family": "ipv4",
        },
        {
            "name": "test_prefix_list3",
            "description": "prefix_list_desc3",
            "comments": "prefix_list_comment3",
            "family": "ipv6",
        },
    ]

    bulk_update_data = {
        "description": "Test Prefix list desc",
    }

    @classmethod
    def setUpTestData(cls):

        prefix_lists = (
            PrefixList(
                name="prefix_list 1",
                description="prefix_list 1",
                comments="prefix_list 1",
                family=IPAddressFamilyChoices.FAMILY_4,
            ),
            PrefixList(
                name="prefix_list 2",
                description="prefix_list 2",
                comments="prefix_list 2",
                family=IPAddressFamilyChoices.FAMILY_6,
            ),
            PrefixList(
                name="prefix_list 3",
                description="prefix_list 3",
                comments="prefix_list 3",
                family=IPAddressFamilyChoices.FAMILY_4,
            ),
        )
        PrefixList.objects.bulk_create(prefix_lists)


class PrefixListRuleAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APIViewTestCases.GraphQLTestCase,
):
    model = PrefixListRule
    view_namespace = "plugins-api:netbox_bgp"
    brief_fields = ["description", "display", "id"]
    graphql_base_name = "netbox_bgp_prefixlist_rule"

    user_permissions = [
        "netbox_bgp.view_prefixlist",
    ]

    bulk_update_data = {"description": "Test Prefix list rules desc", "action": "deny"}

    @classmethod
    def setUpTestData(cls):
        pl1 = PrefixList.objects.create(
            name="pl1", description="test_pl1", family=IPAddressFamilyChoices.FAMILY_4
        )
        pl2 = PrefixList.objects.create(
            name="pl2", description="test_pl2", family=IPAddressFamilyChoices.FAMILY_4
        )
        subnet1 = Prefix.objects.create(prefix="10.0.0.0/24")
        subnet2 = Prefix.objects.create(prefix="10.0.0.0/24")

        prefix_list_rules = (
            PrefixListRule(
                prefix_list=pl1,
                index=10,
                action=ActionChoices._choices[0][0],
                prefix=subnet1,
                ge=24,
                le=32,
                description="pl_rule_1",
                comments="pl_rule_1",
            ),
            PrefixListRule(
                prefix_list=pl1,
                index=20,
                action=ActionChoices._choices[0][0],
                prefix=subnet2,
                ge=24,
                le=32,
                description="pl_rule_2",
                comments="pl_rule_2",
            ),
            PrefixListRule(
                prefix_list=pl1,
                index=30,
                action=ActionChoices._choices[0][1],
                prefix_custom="0.0.0.0/0",
                ge=8,
                le=32,
                description="pl_rule_3",
                comments="pl_rule_3",
            ),
        )
        PrefixListRule.objects.bulk_create(prefix_list_rules)

        cls.create_data = [
            {
                "prefix_list": pl2.id,
                "description": "rule4",
                "index": 10,
                "action": "permit",
                "comments": "rule4",
                "prefix": subnet1.id,
                "ge": 25,
                "le": 32,
            },
            {
                "prefix_list": pl2.id,
                "description": "rule5",
                "index": 20,
                "action": "permit",
                "comments": "rule5",
                "prefix": subnet2.id,
                "ge": 26,
                "le": 32,
            },
            {
                "prefix_list": pl2.id,
                "description": "rule6",
                "index": 30,
                "action": "deny",
                "comments": "rule6",
                "prefix_custom": "0.0.0.0/0",
            },
        ]


class TestAPISchema(APITestCase):
    def test_api_schema(self):
        url = reverse("plugins-api:netbox_bgp-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, 200)
