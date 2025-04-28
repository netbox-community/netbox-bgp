import strawberry_django
from netbox.graphql.filter_mixins import BaseFilterMixin

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
    "CommunityFilter",
    "BGPSessionFilter",
    "BGPPeerGroupFilter",
    "RoutingPolicyFilter",
    "RoutingPolicyRuleFilter",
    "PrefixListFilter",
    "PrefixListRuleFilter",
    "CommunityListFilter",
    "CommunityListRuleFilter",
)


@strawberry_django.filter(Community, lookups=True)
class CommunityFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(BGPSession, lookups=True)
class BGPSessionFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(BGPPeerGroup, lookups=True)
class BGPPeerGroupFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(RoutingPolicy, lookups=True)
class RoutingPolicyFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(RoutingPolicyRule, lookups=True)
class RoutingPolicyRuleFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(PrefixList, lookups=True)
class PrefixListFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(PrefixListRule, lookups=True)
class PrefixListRuleFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(CommunityList, lookups=True)
class CommunityListFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(CommunityListRule, lookups=True)
class CommunityListRuleFilter(BaseFilterMixin):
    pass
