from utilities.testing import ViewTestCases
from ipam.models import Prefix

from netbox_bgp.models import (
    ASPathList,
    ASPathListRule,
    PrefixList,
    PrefixListRule,
    RoutingPolicy,
    RoutingPolicyRule,
    Community,
    CommunityList
)


class ASPathListRuleTestCase(ViewTestCases.BulkImportObjectsViewTestCase):
    model = ASPathListRule

    def _get_base_url(self):
        return 'plugins:{}:{}_{{}}'.format(
            self.model._meta.app_label,
            self.model._meta.model_name
        )
 
    @classmethod
    def setUpTestData(cls):
        aspathlists = [
            ASPathList(name='aspathlist1'),
            ASPathList(name='aspathlist2'),
        ]
        ASPathList.objects.bulk_create(aspathlists)
        aspathlistrules = [
            ASPathListRule(aspath_list=aspathlists[0],index=5,action='permit',pattern='65000')
        ]
        ASPathListRule.objects.bulk_create(aspathlistrules)
        cls.csv_data = (
            "aspath_list,index,action,pattern",
            f"{aspathlists[0].name},10,permit,65001",
            f"{aspathlists[1].name},20,permit,65002",
        )
        cls.csv_update_data = (
            "id,aspath_list,index,action,pattern",
            f"{aspathlistrules[0].pk},{aspathlists[0].name},5,deny,65000",
        )

class PrefixListRuleTestCase(ViewTestCases.BulkImportObjectsViewTestCase):
    model = PrefixListRule

    def _get_base_url(self):
        return 'plugins:{}:{}_{{}}'.format(
            self.model._meta.app_label,
            self.model._meta.model_name
        )
 
    @classmethod
    def setUpTestData(cls):
        prefixes = [
            Prefix(prefix='1.1.1.0/24'),
            Prefix(prefix='2.2.2.0/24')
        ]
        Prefix.objects.bulk_create(prefixes)
        prefixlists = [
            PrefixList(name='prefixlist1'),
            PrefixList(name='prefixlist2'),
        ]
        PrefixList.objects.bulk_create(prefixlists)
        prefixlistrules = [
            PrefixListRule(prefix_list=prefixlists[0], index=5, action='permit', prefix=prefixes[0])
        ]
        PrefixListRule.objects.bulk_create(prefixlistrules)
        cls.csv_data = (
            "prefix_list,index,action,prefix",
            f"{prefixlists[0].name},10,permit,{prefixes[0].prefix}",
            f"{prefixlists[1].name},10,permit,{prefixes[1].prefix}",
        )
        cls.csv_update_data = (
            "id,prefix_list,index,action",
            f"{prefixlistrules[0].pk},{prefixlists[0].name},5,deny",
        )

class RoutingPolicyRuleTestCase(ViewTestCases.BulkImportObjectsViewTestCase):
    model = RoutingPolicyRule

    def _get_base_url(self):
        return 'plugins:{}:{}_{{}}'.format(
            self.model._meta.app_label,
            self.model._meta.model_name
        )
 
    @classmethod
    def setUpTestData(cls):
        aspathlists = [
            ASPathList(name='aspathlist1'),
        ]
        ASPathList.objects.bulk_create(aspathlists)
        prefixlists = [
            PrefixList(name='prefixlist1'),
            PrefixList(name='prefixlist2'),
        ]
        PrefixList.objects.bulk_create(prefixlists)
        rps = [
            RoutingPolicy(name='rp1'),
            RoutingPolicy(name='rp2'),
        ]
        RoutingPolicy.objects.bulk_create(rps)
        communities = [
            Community(value='65001:1')
        ]
        Community.objects.bulk_create(communities)
        comm_lists = [
            CommunityList(name='cl1')
        ]
        CommunityList.objects.bulk_create(comm_lists)
        rp_rules = [
            RoutingPolicyRule(routing_policy=rps[0], index=10, action='permit')
        ]
        RoutingPolicyRule.objects.bulk_create(rp_rules)

        cls.csv_data = (
            "routing_policy,index,action,match_community,match_community_list,match_aspath_list,match_ip_address,match_ipv6_address",
            f"{rps[0].name},20,permit,{communities[0].value},{comm_lists[0].name},{aspathlists[0].name},{prefixlists[0].name},{prefixlists[1].name}",
            f"{rps[1].name},10,permit,{communities[0].value},{comm_lists[0].name},{aspathlists[0].name},{prefixlists[0].name},{prefixlists[1].name}",
        )
        cls.csv_update_data = (
            "id,routing_policy,index,action",
            f"{rp_rules[0].pk},{rps[0].name},10,deny",
        )
