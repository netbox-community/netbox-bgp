from netbox.search import SearchIndex

from netbox_bgp.models import (
    ASPathList,
    BGPPeerGroup,
    BGPSession,
    Community,
    CommunityList,
    PrefixList,
    RoutingPolicy,
)


class BGPSessionIndex(SearchIndex):
    model = BGPSession
    fields = (
        ('name', 100),
        ('description', 500),
        ('remote_as_macro', 500),
        ('comments', 5000),
    )
    display_attrs = ('device', 'virtualmachine', 'site', 'status', 'tenant', 'description')


class BGPPeerGroupIndex(SearchIndex):
    model = BGPPeerGroup
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('description',)


class CommunityIndex(SearchIndex):
    model = Community
    fields = (
        ('value', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('status', 'site', 'tenant', 'description')


class CommunityListIndex(SearchIndex):
    model = CommunityList
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('description',)


class RoutingPolicyIndex(SearchIndex):
    model = RoutingPolicy
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('description',)


class PrefixListIndex(SearchIndex):
    model = PrefixList
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('family', 'description')


class ASPathListIndex(SearchIndex):
    model = ASPathList
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('description',)


indexes = [
    BGPSessionIndex,
    BGPPeerGroupIndex,
    CommunityIndex,
    CommunityListIndex,
    RoutingPolicyIndex,
    PrefixListIndex,
    ASPathListIndex,
]
