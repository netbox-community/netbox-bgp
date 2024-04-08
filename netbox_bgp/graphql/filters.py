import strawberry_django
from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

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
@autotype_decorator(CommunityFilterSet)
class CommunityFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(BGPSession, lookups=True)
@autotype_decorator(BGPSessionFilterSet)
class BGPSessionFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(BGPPeerGroup, lookups=True)
@autotype_decorator(BGPPeerGroupFilterSet)
class BGPPeerGroupFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(RoutingPolicy, lookups=True)
@autotype_decorator(RoutingPolicyFilterSet)
class RoutingPolicyFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(RoutingPolicyRule, lookups=True)
@autotype_decorator(RoutingPolicyRuleFilterSet)
class RoutingPolicyRuleFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(PrefixList, lookups=True)
@autotype_decorator(PrefixListFilterSet)
class PrefixListFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(PrefixListRule, lookups=True)
@autotype_decorator(PrefixListRuleFilterSet)
class PrefixListRuleFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(CommunityList, lookups=True)
@autotype_decorator(CommunityListFilterSet)
class CommunityListFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(CommunityListRule, lookups=True)
@autotype_decorator(CommunityListRuleFilterSet)
class CommunityListRuleFilter(BaseFilterMixin):
    pass
