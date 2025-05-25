import strawberry
import strawberry_django
from strawberry.scalars import ID
from strawberry_django import FilterLookup

from typing import Annotated
from netbox.graphql.filter_mixins import NetBoxModelFilterMixin
from tenancy.graphql.filter_mixins import TenancyFilterMixin



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
)


@strawberry_django.filter(Community, lookups=True)
class NetBoxBGPCommunityFilter(TenancyFilterMixin, NetBoxModelFilterMixin):
    value: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    status: (
        Annotated[
            "NetBoxBGPCommunityStatusEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(BGPSession, lookups=True)
class NetBoxBGPSessionFilter(TenancyFilterMixin, NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
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




@strawberry_django.filter(BGPPeerGroup, lookups=True)
class NetBoxBGPBGPPeerGroupFilter(NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()

@strawberry_django.filter(RoutingPolicy, lookups=True)
class NetBoxBGPRoutingPolicyFilter(NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()

@strawberry_django.filter(RoutingPolicyRule, lookups=True)
class NetBoxBGPRoutingPolicyRuleFilter(NetBoxModelFilterMixin):
    description: FilterLookup[str] | None = strawberry_django.filter_field()   
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


@strawberry_django.filter(PrefixList, lookups=True)
class NetBoxBGPPrefixListFilter(NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    family: (
        Annotated[
            "NetBoxBGPIPAddressFamilyEnum", strawberry.lazy("netbox_bgp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(PrefixListRule, lookups=True)
class NetBoxBGPPrefixListRuleFilter(NetBoxModelFilterMixin):
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



@strawberry_django.filter(CommunityList, lookups=True)
class NetBoxBGPCommunityListFilter(NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(CommunityListRule, lookups=True)
class NetBoxBGPCommunityListRuleFilter(NetBoxModelFilterMixin):
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



