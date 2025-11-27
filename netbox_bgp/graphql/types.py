from typing import Annotated, List, TYPE_CHECKING, Optional, Union
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
    ASPathList,
    ASPathListRule,
    Redistributing,
)
from .filters import (
    NetBoxBGPCommunityFilter,
    NetBoxBGPSessionFilter,
    NetBoxBGPBGPPeerGroupFilter,
    NetBoxBGPRoutingPolicyFilter,
    NetBoxBGPRoutingPolicyRuleFilter,
    NetBoxBGPPrefixListFilter,
    NetBoxBGPPrefixListRuleFilter,
    NetBoxBGPCommunityListFilter,
    NetBoxBGPCommunityListRuleFilter,
    NetBoxBGPASPathListFilter,
    NetBoxBGPASPathListRuleFilter,
    NetBoxBGPRedistributingFilter,
)


@strawberry_django.type(ASPathList, fields="__all__", filters=NetBoxBGPASPathListFilter)
class ASPathListType(NetBoxObjectType):
    name: str
    description: str
    rules: List[
         Annotated["ASPathListRuleType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]

    @strawberry_django.field
    def scope(self) -> Annotated[Union[
        Annotated["ClusterType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["ClusterGroupType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["LocationType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RackType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RegionType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteGroupType", strawberry.lazy('dcim.graphql.types')],
    ], strawberry.union("CommunityScopeType")] | None:
        return self.scope


@strawberry_django.type(ASPathListRule, fields="__all__", filters=NetBoxBGPASPathListRuleFilter)
class ASPathListRuleType(NetBoxObjectType):
    aspath_list: Annotated[
        "ASPathListType", strawberry.lazy("netbox_bgp.graphql.types")
    ]
    index: BigInt
    action: str
    pattern: str
    description: str


@strawberry_django.type(Community, fields="__all__", filters=NetBoxBGPCommunityFilter)
class CommunityType(NetBoxObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    status: str
    role: Annotated["RoleType", strawberry.lazy("ipam.graphql.types")] | None
    description: str

    @strawberry_django.field
    def scope(self) -> Annotated[Union[
        Annotated["ClusterType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["ClusterGroupType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["LocationType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RackType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RegionType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteGroupType", strawberry.lazy('dcim.graphql.types')],
    ], strawberry.union("CommunityScopeType")] | None:
        return self.scope


@strawberry_django.type(BGPSession, fields="__all__", filters=NetBoxBGPSessionFilter)
class BGPSessionType(NetBoxObjectType):
    name: str
    site: Annotated["SiteType", strawberry.lazy("dcim.graphql.types")] | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    device: Annotated["DeviceType", strawberry.lazy("dcim.graphql.types")] | None
    virtualmachine: Annotated["VirtualMachineType", strawberry.lazy("virtualization.graphql.types")] | None
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
    prefix_list_in: Annotated["PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")] | None
    prefix_list_out: Annotated["PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")] | None


@strawberry_django.type(BGPPeerGroup, fields="__all__", filters=NetBoxBGPBGPPeerGroupFilter)
class BGPPeerGroupType(NetBoxObjectType):
    name: str
    description: str
    import_policies: List[
        Annotated["RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    export_policies: List[
        Annotated["RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]

    @strawberry_django.field
    def scope(self) -> Annotated[Union[
        Annotated["ClusterType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["ClusterGroupType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["LocationType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RackType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RegionType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteGroupType", strawberry.lazy('dcim.graphql.types')],
    ], strawberry.union("BGPPeerGroupScopeType")] | None:
        return self.scope


@strawberry_django.type(RoutingPolicy, fields="__all__", filters=NetBoxBGPRoutingPolicyFilter)
class RoutingPolicyType(NetBoxObjectType):
    name: str
    description: str
    weight: int | None
    rules: List[
         Annotated["RoutingPolicyRuleType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]

    @strawberry_django.field
    def scope(self) -> Annotated[Union[
        Annotated["ClusterType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["ClusterGroupType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["LocationType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RackType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RegionType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteGroupType", strawberry.lazy('dcim.graphql.types')],
    ], strawberry.union("RoutingPolicyScopeType")] | None:
        return self.scope


@strawberry_django.type(
    RoutingPolicyRule, fields="__all__", filters=NetBoxBGPRoutingPolicyRuleFilter
)
class RoutingPolicyRuleType(NetBoxObjectType):
    routing_policy: Annotated[
        "RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")
    ]
    index: BigInt
    action: str
    description: str
    continue_entry: BigInt | None
    match_community: List[
        Annotated["CommunityType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    match_community_list: List[
        Annotated["CommunityListType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    match_aspath_list: List[
        Annotated["ASPathListType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    match_ip_address: List[
        Annotated["PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]
    match_ipv6_address: List[
        Annotated["PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]


@strawberry_django.type(PrefixList, fields="__all__", filters=NetBoxBGPPrefixListFilter)
class PrefixListType(NetBoxObjectType):
    name: str
    description: str
    family: str
    prefrules: List[
         Annotated["PrefixListRuleType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]

    @strawberry_django.field
    def scope(self) -> Annotated[Union[
        Annotated["ClusterType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["ClusterGroupType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["LocationType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RackType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RegionType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteGroupType", strawberry.lazy('dcim.graphql.types')],
    ], strawberry.union("PrefixListScopeType")] | None:
        return self.scope


@strawberry_django.type(PrefixListRule, fields="__all__", filters=NetBoxBGPPrefixListRuleFilter)
class PrefixListRuleType(NetBoxObjectType):
    prefix_list: Annotated[
        "PrefixListType", strawberry.lazy("netbox_bgp.graphql.types")
    ]
    index: BigInt
    action: str
    prefix: Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")] | None
    prefix_custom: str | None
    ge: BigInt
    le: BigInt
    description: str


@strawberry_django.type(CommunityList, fields="__all__", filters=NetBoxBGPCommunityListFilter)
class CommunityListType(NetBoxObjectType):
    name: str
    description: str
    commlistrules: List[
         Annotated["CommunityListRuleType", strawberry.lazy("netbox_bgp.graphql.types")]
    ]

    @strawberry_django.field
    def scope(self) -> Annotated[Union[
        Annotated["ClusterType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["ClusterGroupType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["LocationType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RackType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RegionType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteGroupType", strawberry.lazy('dcim.graphql.types')],
    ], strawberry.union("CommunityListScopeType")] | None:
        return self.scope


@strawberry_django.type(
    CommunityListRule, fields="__all__", filters=NetBoxBGPCommunityListRuleFilter
)
class CommunityListRuleType(NetBoxObjectType):
    community_list: Annotated[
        "CommunityListType", strawberry.lazy("netbox_bgp.graphql.types")
    ]
    action: str
    community: Annotated["CommunityType", strawberry.lazy("netbox_bgp.graphql.types")]
    description: str


@strawberry_django.type(Redistributing, fields="__all__", filters=NetBoxBGPRedistributingFilter)
class RedistributingType(NetBoxObjectType):
    name: str
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    device: Annotated["DeviceType", strawberry.lazy("dcim.graphql.types")] | None
    virtualmachine: Annotated["VirtualMachineType", strawberry.lazy("virtualization.graphql.types")] | None
    description: str
    redistribute_source: str
    redistribute_policy: (
        Annotated["RoutingPolicyType", strawberry.lazy("netbox_bgp.graphql.types")]
    )

    @strawberry_django.field
    def scope(self) -> Annotated[Union[
        Annotated["ClusterType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["ClusterGroupType", strawberry.lazy('virtualization.graphql.types')],
        Annotated["LocationType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RackType", strawberry.lazy('dcim.graphql.types')],
        Annotated["RegionType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteType", strawberry.lazy('dcim.graphql.types')],
        Annotated["SiteGroupType", strawberry.lazy('dcim.graphql.types')],
    ], strawberry.union("RedistributingScopeType")] | None:
        return self.scope
