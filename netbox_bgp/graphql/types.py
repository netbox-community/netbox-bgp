from typing import Annotated, List

import strawberry
import strawberry_django


from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.scalars import BigInt

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
from .filters import (
    CommunityFilter,
    BGPSessionFilter,
    BGPPeerGroupFilter,
    RoutingPolicyFilter,
    RoutingPolicyRuleFilter,
    PrefixListFilter,
    PrefixListRuleFilter,
    CommunityListFilter,
    CommunityListRuleFilter,
)


@strawberry_django.type(Community, fields="__all__", filters=CommunityFilter)
class CommunityType(NetBoxObjectType):
    site: Annotated["SiteType", strawberry.lazy("dcim.graphql.types")] | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    status: str
    role: str
    description: str


@strawberry_django.type(BGPSession, fields="__all__", filters=BGPSessionFilter)
class BGPSessionType(NetBoxObjectType):
    name: str
    site: Annotated["SiteType", strawberry.lazy("dcim.graphql.types")] | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    device: Annotated["DeviceType", strawberry.lazy("dcim.graphql.types")]
    local_address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")]
    remote_address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")]
    local_as: Annotated["ASNType", strawberry.lazy("ipam.graphql.types")]
    remote_as: Annotated["ASNType", strawberry.lazy("ipam.graphql.types")]
    status: str
    description: str
    peer_group: (
        Annotated["BGPPeerGroupType", strawberry.lazy("netbox_bgp.graphql.types")]
        | None
    )
    import_policies: List[
        Annotated["RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    export_policies: List[
        Annotated["RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    prefix_list_in: List[
        Annotated["PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    prefix_list_out: List[
        Annotated["PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]


@strawberry_django.type(BGPPeerGroup, fields="__all__", filters=BGPPeerGroupFilter)
class BGPPeerGroupType(NetBoxObjectType):
    name: str
    description: str
    import_policies: List[
        Annotated["RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    export_policies: List[
        Annotated["RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]


@strawberry_django.type(RoutingPolicy, fields="__all__", filters=RoutingPolicyFilter)
class RoutingPolicyType(NetBoxObjectType):
    name: str
    description: str


@strawberry_django.type(
    RoutingPolicyRule, fields="__all__", filters=RoutingPolicyRuleFilter
)
class RoutingPolicyRuleType(NetBoxObjectType):
    routing_policy: Annotated[
        "RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")
    ]
    index: BigInt
    action: str
    description: str
    continue_entry: BigInt
    match_community: List[
        Annotated["CommunityType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    match_community_list: List[
        Annotated["CommunityListType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    match_ip_address: List[
        Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]
    ]
    match_ipv6_address: List[
        Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]
    ]


@strawberry_django.type(PrefixList, fields="__all__", filters=PrefixListFilter)
class PrefixListType(NetBoxObjectType):
    name: str
    description: str
    family: str


@strawberry_django.type(PrefixListRule, fields="__all__", filters=PrefixListRuleFilter)
class PrefixListRuleType(NetBoxObjectType):
    prefix_list: Annotated[
        "PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")
    ]
    index: BigInt
    action: str
    prefix: Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]
    prefix_custom: str
    ge: BigInt
    le: BigInt
    description: str


@strawberry_django.type(CommunityList, fields="__all__", filters=CommunityListFilter)
class CommunityListType(NetBoxObjectType):
    name: str
    description: str


@strawberry_django.type(
    CommunityListRule, fields="__all__", filters=CommunityListRuleFilter
)
class CommunityListRuleType(NetBoxObjectType):
    community_list: Annotated[
        "CommunityListType", strawberry.lazy("netbox_bgp.graphql.types")
    ]
    action: str
    community: Annotated["CommunityType", strawberry.lazy("netbox_bgp.graphql.types")]
    description: str
