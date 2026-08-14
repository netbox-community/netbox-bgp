import strawberry
import strawberry_django
from strawberry.scalars import ID

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from strawberry_django import FilterLookup

from typing import Annotated
from netbox.graphql.filters import NetBoxModelFilter
from tenancy.graphql.filter_mixins import TenancyFilterMixin
from ipam.graphql.filters import IPAddressFilter, ASNFilter
from dcim.graphql.filters import DeviceFilter

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
    ASPathListRule
)

from netbox_bgp.filtersets import (
    CommunityFilterSet,
    BGPSessionFilterSet,
    BGPPeerGroupFilterSet,
    RoutingPolicyFilterSet,
    RoutingPolicyRuleFilterSet,
    PrefixListFilterSet,
    PrefixListRuleFilterSet,
    CommunityListFilterSet,
    CommunityListRuleFilterSet,
    ASPathListFilterSet,
    ASPathListRuleFilterSet
)

from netbox_bgp.graphql.enums import (
    NetBoxBGPCommunityStatusEnum,
    NetBoxBGPSessionStatusEnum,
    NetBoxBGPIPAddressFamilyEnum,
    NetBoxBGPActionEnum
)


__all__ = (
    "NetBoxBGPCommunityFilter",
    "NetBoxBGPSessionFilter",
    "NetBoxBGPBGPPeerGroupFilter",
    "NetBoxBGPRoutingPolicyFilter",
    "NetBoxBGPRoutingPolicyRuleFilter",
    "NetBoxBGPPrefixListFilter",
    "NetBoxBGPPrefixListRuleFilter",
    "NetBoxBGPCommunityListFilter",
    "NetBoxBGPCommunityListRuleFilter",
    "NetBoxBGPASPathListFilter",
    "NetBoxBGPASPathListRuleFilter",
    # Conventional <Model>Filter aliases (see bottom of module)
    "ASPathListFilter",
    "ASPathListRuleFilter",
    "BGPPeerGroupFilter",
    "BGPSessionFilter",
    "CommunityFilter",
    "CommunityListFilter",
    "CommunityListRuleFilter",
    "PrefixListFilter",
    "PrefixListRuleFilter",
    "RoutingPolicyFilter",
    "RoutingPolicyRuleFilter",
)

@strawberry_django.filter_type(ASPathList, lookups=True)
class NetBoxBGPASPathListFilter(NetBoxModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()

@strawberry_django.filter_type(ASPathListRule, lookups=True)
class NetBoxBGPASPathListRuleFilter(NetBoxModelFilter):
    value: StrFilterLookup[str] | None = strawberry_django.filter_field()
    aspath_list: (
        Annotated[
            "NetBoxBGPASPathListFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    aspath_list_id: ID | None = strawberry_django.filter_field()
    action: (
        Annotated[
            "NetBoxBGPActionEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()

@strawberry_django.filter_type(Community, lookups=True)
class NetBoxBGPCommunityFilter(TenancyFilterMixin, NetBoxModelFilter):
    value: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    status: (
        Annotated[
            "NetBoxBGPCommunityStatusEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter_type(BGPSession, lookups=True)
class NetBoxBGPSessionFilter(TenancyFilterMixin, NetBoxModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    status: (
        Annotated[
            "NetBoxBGPSessionStatusEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()

    remote_as: (
        Annotated["ASNFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    remote_as_id: ID | None = strawberry_django.filter_field()

    remote_as_macro: StrFilterLookup[str] | None = strawberry_django.filter_field()

    local_as: (
        Annotated["ASNFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    local_as_id: ID | None = strawberry_django.filter_field()

    local_address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    local_address_id: ID | None = strawberry_django.filter_field()

    remote_address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    remote_address_id: ID | None = strawberry_django.filter_field()

    remote_prefix: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    remote_prefix_id: ID | None = strawberry_django.filter_field()

    device: (
        Annotated["DeviceFilter", strawberry.lazy("dcim.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()

    peer_group: (
        Annotated[
            "NetBoxBGPBGPPeerGroupFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()

    import_policies: (
        Annotated[
            "NetBoxBGPRoutingPolicyFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()

    export_policies: (
        Annotated[
            "NetBoxBGPRoutingPolicyFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()

    max_prefixes: FilterLookup[int] | None = strawberry_django.filter_field()


@strawberry_django.filter_type(BGPPeerGroup, lookups=True)
class NetBoxBGPBGPPeerGroupFilter(NetBoxModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()

@strawberry_django.filter_type(RoutingPolicy, lookups=True)
class NetBoxBGPRoutingPolicyFilter(NetBoxModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()

@strawberry_django.filter_type(RoutingPolicyRule, lookups=True)
class NetBoxBGPRoutingPolicyRuleFilter(NetBoxModelFilter):
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    routing_policy: (
        Annotated[
            "NetBoxBGPRoutingPolicyFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    routing_policy_id: ID | None = strawberry_django.filter_field()
    action: (
        Annotated[
            "NetBoxBGPActionEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    aspath_list: (
        Annotated[
            "NetBoxBGPASPathListFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    aspath_list_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter_type(PrefixList, lookups=True)
class NetBoxBGPPrefixListFilter(NetBoxModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    family: (
        Annotated[
            "NetBoxBGPIPAddressFamilyEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter_type(PrefixListRule, lookups=True)
class NetBoxBGPPrefixListRuleFilter(NetBoxModelFilter):
    action: (
        Annotated[
            "NetBoxBGPActionEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    prefix_list: (
        Annotated[
            "NetBoxBGPPrefixListFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    prefix_list_id: ID | None = strawberry_django.filter_field()



@strawberry_django.filter_type(CommunityList, lookups=True)
class NetBoxBGPCommunityListFilter(NetBoxModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter_type(CommunityListRule, lookups=True)
class NetBoxBGPCommunityListRuleFilter(NetBoxModelFilter):
    action: (
        Annotated[
            "NetBoxBGPActionEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()

    community_list: (
        Annotated[
            "NetBoxBGPCommunityListFilter", strawberry.lazy("netbox_bgp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    community_list_id: ID | None = strawberry_django.filter_field()


# NetBox discovers a model's GraphQL filter class at the conventional path
# <app_label>.graphql.filters.<Model>Filter (utilities.testing.api). These aliases
# expose the prefixed classes above under those names; the GraphQL type names are
# taken from the decorated class at definition time, so the schema is unchanged.
ASPathListFilter = NetBoxBGPASPathListFilter
ASPathListRuleFilter = NetBoxBGPASPathListRuleFilter
BGPPeerGroupFilter = NetBoxBGPBGPPeerGroupFilter
BGPSessionFilter = NetBoxBGPSessionFilter
CommunityFilter = NetBoxBGPCommunityFilter
CommunityListFilter = NetBoxBGPCommunityListFilter
CommunityListRuleFilter = NetBoxBGPCommunityListRuleFilter
PrefixListFilter = NetBoxBGPPrefixListFilter
PrefixListRuleFilter = NetBoxBGPPrefixListRuleFilter
RoutingPolicyFilter = NetBoxBGPRoutingPolicyFilter
RoutingPolicyRuleFilter = NetBoxBGPRoutingPolicyRuleFilter


