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
from .types import *


@strawberry.type
class NetBoxBGPQuery:
    @strawberry.field
    def community(self, id: int) -> CommunityType:
        return Community.objects.get(pk=id)

    community_list: List[CommunityType] = strawberry_django.field()

    @strawberry.field
    def bgp_session(self, id: int) -> BGPSessionType:
        return BGPSession.objects.get(pk=id)

    bgp_session_list: List[BGPSessionType] = strawberry_django.field()

    @strawberry.field
    def bgp_peer_group(self, id: int) -> BGPPeerGroupType:
        return BGPPeerGroup.objects.get(pk=id)

    bgp_peer_group_list: List[BGPPeerGroupType] = strawberry_django.field()

    @strawberry.field
    def bgp_peer_group(self, id: int) -> RoutingPolicyType:
        return RoutingPolicy.objects.get(pk=id)

    routing_policies_list: List[RoutingPolicyType] = strawberry_django.field()

    @strawberry.field
    def bgp_peer_group(self, id: int) -> RoutingPolicyRuleType:
        return RoutingPolicyRule.objects.get(pk=id)

    routing_policies_rules_list: List[RoutingPolicyRuleType] = strawberry_django.field()

    @strawberry.field
    def bgp_peer_group(self, id: int) -> PrefixListType:
        return PrefixList.objects.get(pk=id)

    prefixlist_list: List[PrefixListType] = strawberry_django.field()

    @strawberry.field
    def bgp_peer_group(self, id: int) -> PrefixListRuleType:
        return PrefixListRule.objects.get(pk=id)

    prefixlist_rules_list: List[PrefixListRuleType] = strawberry_django.field()

    @strawberry.field
    def bgp_peer_group(self, id: int) -> CommunityListType:
        return CommunityList.objects.get(pk=id)

    communitylist_list: List[CommunityListType] = strawberry_django.field()

    @strawberry.field
    def bgp_peer_group(self, id: int) -> CommunityListRuleType:
        return CommunityListRule.objects.get(pk=id)

    communitylist_rules_list: List[CommunityListRuleType] = strawberry_django.field()
