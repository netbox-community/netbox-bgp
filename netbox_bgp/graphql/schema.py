from typing import List

import strawberry
import strawberry_django

from netbox_bgp.models import (
    Community,
    BGPSession,
    RoutingPolicy,
    BGPPeerGroup,
    RoutingPolicyRule,
    PrefixList,
    PrefixListRule,
    CommunityList,
    CommunityListRule,
)
from .types import (
    CommunityType,
    BGPSessionType,
    BGPPeerGroupType,
    RoutingPolicyType,
    RoutingPolicyRuleType,
    PrefixListType,
    PrefixListRuleType,
    CommunityListType,
    CommunityListRuleType,
)


@strawberry.type
class NetBoxBGPQuery:
    @strawberry.field
    def netbox_bgp_community(self, id: int) -> CommunityType:
        return Community.objects.get(pk=id)

    netbox_bgp_community_list: List[CommunityType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_session(self, id: int) -> BGPSessionType:
        return BGPSession.objects.get(pk=id)

    netbox_bgp_session_list: List[BGPSessionType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_peer_group(self, id: int) -> BGPPeerGroupType:
        return BGPPeerGroup.objects.get(pk=id)

    netbox_bgp_peer_group_list: List[BGPPeerGroupType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_routing_policy(self, id: int) -> RoutingPolicyType:
        return RoutingPolicy.objects.get(pk=id)

    netbox_bgp_routing_policy_list: List[RoutingPolicyType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_routing_policy_rule(self, id: int) -> RoutingPolicyRuleType:
        return RoutingPolicyRule.objects.get(pk=id)

    netbox_bgp_routing_policy_rule_list: List[RoutingPolicyRuleType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_prefixlist(self, id: int) -> PrefixListType:
        return PrefixList.objects.get(pk=id)

    netbox_bgp_prefixlist_list: List[PrefixListType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_prefixlist_rule(self, id: int) -> PrefixListRuleType:
        return PrefixListRule.objects.get(pk=id)

    netbox_bgp_prefixlist_rule_list: List[PrefixListRuleType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_communitylist(self, id: int) -> CommunityListType:
        return CommunityList.objects.get(pk=id)

    netbox_bgp_communitylist_list: List[CommunityListType] = strawberry_django.field()

    @strawberry.field
    def netbox_bgp_communitylist_rule(self, id: int) -> CommunityListRuleType:
        return CommunityListRule.objects.get(pk=id)

    netbox_bgp_communitylist_rule_list: List[CommunityListRuleType] = strawberry_django.field()
