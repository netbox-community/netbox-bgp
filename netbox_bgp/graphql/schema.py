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


@strawberry.type(name="Query")
class NetBoxBGPQuery:

    netbox_bgp_community: CommunityType = strawberry_django.field()
    netbox_bgp_community_list: List[CommunityType] = strawberry_django.field()

    netbox_bgp_session: BGPSessionType = strawberry_django.field()
    netbox_bgp_session_list: List[BGPSessionType] = strawberry_django.field()

    netbox_bgp_peer_group: BGPPeerGroupType = strawberry_django.field()
    netbox_bgp_peer_group_list: List[BGPPeerGroupType] = strawberry_django.field()

    netbox_bgp_routing_policy: RoutingPolicyType = strawberry_django.field()
    netbox_bgp_routing_policy_list: List[RoutingPolicyType] = strawberry_django.field()

    netbox_bgp_routing_policy_rule: RoutingPolicyRuleType = strawberry_django.field()
    netbox_bgp_routing_policy_rule_list: List[RoutingPolicyRuleType] = strawberry_django.field()

    netbox_bgp_prefixlist: PrefixListType = strawberry_django.field()
    netbox_bgp_prefixlist_list: List[PrefixListType] = strawberry_django.field()

    netbox_bgp_prefixlist_rule: PrefixListRuleType = strawberry_django.field()
    netbox_bgp_prefixlist_rule_list: List[PrefixListRuleType] = strawberry_django.field()

    netbox_bgp_communitylist: CommunityListType = strawberry_django.field()
    netbox_bgp_communitylist_list: List[CommunityListType] = strawberry_django.field()

    netbox_bgp_communitylist_rule: CommunityListRuleType = strawberry_django.field()
    netbox_bgp_communitylist_rule_list: List[CommunityListRuleType] = strawberry_django.field()
