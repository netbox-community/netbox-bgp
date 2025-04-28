from django.urls import include, path
from utilities.urls import get_model_urls

from .models import (
    BGPSession, Community, RoutingPolicy,
    BGPPeerGroup, RoutingPolicyRule, PrefixList,
    PrefixListRule, CommunityList, CommunityListRule
)
from . import views

app_name = 'netbox_bgp'

urlpatterns = (
    # Community
    path(
        "community/",
        include(get_model_urls("netbox_bgp", "community", detail=False)),
    ),
    path(
        "community/<int:pk>/",
        include(get_model_urls("netbox_bgp", "community")),
    ),

    # Community Lists
    path(
        "community-list/",
        include(get_model_urls("netbox_bgp", "communitylist", detail=False)),
    ),
    path(
        "community-list/<int:pk>/",
        include(get_model_urls("netbox_bgp", "communitylist")),
    ),

    # Community List Rules
    path(
        "community-list-rule/",
        include(get_model_urls("netbox_bgp", "communitylistrule", detail=False)),
    ),
    path(
        "community-list-rule/<int:pk>/",
        include(get_model_urls("netbox_bgp", "communitylistrule")),
    ),

    # Sessions
    path(
        "session/",
        include(get_model_urls("netbox_bgp", "bgpsession", detail=False)),
    ),
    path(
        "session/<int:pk>/",
        include(get_model_urls("netbox_bgp", "bgpsession")),
    ),

    # Routing Policies
    path(
        "routing-policy/",
        include(get_model_urls("netbox_bgp", "routingpolicy", detail=False)),
    ),
    path(
        "routing-policy/<int:pk>/",
        include(get_model_urls("netbox_bgp", "routingpolicy")),
    ),

    # Routing Policy Rules
    path(
        "routing-policy-rule/",
        include(get_model_urls("netbox_bgp", "routingpolicyrule", detail=False)),
    ),
    path(
        "routing-policy-rule/<int:pk>/",
        include(get_model_urls("netbox_bgp", "routingpolicyrule")),
    ),

    # Peer Groups
    path(
        "peer-group/",
        include(get_model_urls("netbox_bgp", "bgppeergroup", detail=False)),
    ),
    path(
        "peer-group/<int:pk>/",
        include(get_model_urls("netbox_bgp", "bgppeergroup")),
    ),

    # Prefix Lists
    path(
        "prefix-list/",
        include(get_model_urls("netbox_bgp", "prefixlist", detail=False)),
    ),
    path(
        "prefix-list/<int:pk>/",
        include(get_model_urls("netbox_bgp", "prefixlist")),
    ),

    # Prefix List Rules
    path(
        "prefix-list-rule/",
        include(get_model_urls("netbox_bgp", "prefixlistrule", detail=False)),
    ),
    path(
        "prefix-list-rule/<int:pk>/",
        include(get_model_urls("netbox_bgp", "prefixlistrule")),
    ),
)
