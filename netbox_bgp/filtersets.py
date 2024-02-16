import django_filters
import netaddr
from django.db.models import Q
from netaddr.core import AddrFormatError
from extras.filters import TagFilter
from netbox.filtersets import NetBoxModelFilterSet

from .models import (
    Community, BGPSession, RoutingPolicy, RoutingPolicyRule,
    BGPPeerGroup, PrefixList, PrefixListRule, CommunityList,
    CommunityListRule
)
from ipam.models import IPAddress, ASN
from dcim.models import Device, Site


class CommunityFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Community
        fields = ['id', 'value', 'description', 'status', 'tenant']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(value__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class CommunityListFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CommunityList
        fields = ['id', 'name', 'description']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(name__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class CommunityListRuleFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CommunityListRule
        fields = ['id', 'action', 'community_list', 'community_list_id']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(action__icontains=value)
                | Q(community_list__icontains=value)
                | Q(community_list_id__icontains=value)
        )
        return queryset.filter(qs_filter)


class BGPSessionFilterSet(NetBoxModelFilterSet):

    remote_as = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as__asn',
        queryset=ASN.objects.all(),
        to_field_name='asn',
        label='Remote AS (Number)',
    )
    remote_as_id = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as__id',
        queryset=ASN.objects.all(),
        to_field_name='id',
        label='Remote AS (ID)',
    )
    local_as = django_filters.ModelMultipleChoiceFilter(
        field_name='local_as__asn',
        queryset=ASN.objects.all(),
        to_field_name='asn',
        label='Local AS (Number)',
    )
    local_as_id = django_filters.ModelMultipleChoiceFilter(
        field_name='local_as__id',
        queryset=ASN.objects.all(),
        to_field_name='id',
        label='Local AS (ID)',
    )
    peer_group = django_filters.ModelMultipleChoiceFilter(
        queryset=BGPPeerGroup.objects.all(),
    )
    import_policies = django_filters.ModelMultipleChoiceFilter(
        queryset=RoutingPolicy.objects.all(),
    )
    export_policies = django_filters.ModelMultipleChoiceFilter(
        queryset=RoutingPolicy.objects.all(),
    )
    local_address_id = django_filters.ModelMultipleChoiceFilter(
        field_name='local_address__id',
        queryset=IPAddress.objects.all(),
        to_field_name='id',
        label='Local Address (ID)',
    )
    local_address = django_filters.ModelMultipleChoiceFilter(
        field_name='local_address__address',
        queryset=IPAddress.objects.all(),
        to_field_name='address',
        label='Local Address',
    )
    remote_address_id = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_address__id',
        queryset=IPAddress.objects.all(),
        to_field_name='id',
        label='Remote Address (ID)',
    )
    remote_address = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_address__address',
        queryset=IPAddress.objects.all(),
        to_field_name='address',
        label='Remote Address',
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device__id',
        queryset=Device.objects.all(),
        to_field_name='id',
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device (name)',
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        field_name='site__id',
        queryset=Site.objects.all(),
        to_field_name='id',
        label='Site (ID)',
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='site__name',
        queryset=Site.objects.all(),
        to_field_name='name',
        label='DSite (name)',
    )    
    by_remote_address = django_filters.CharFilter(
        method='search_by_remote_ip',
        label='Remote Address',
    )
    by_local_address = django_filters.CharFilter(
        method='search_by_local_ip',
        label='Local Address',
    )

    class Meta:
        model = BGPSession
        fields = ['id', 'name', 'description', 'status', 'tenant']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(remote_as__asn__icontains=value)
                | Q(name__icontains=value)
                | Q(local_as__asn__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)

    def search_by_remote_ip(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(netaddr.IPNetwork(value).cidr)
            return queryset.filter(remote_address__address=query)
        except (AddrFormatError, ValueError):
            return queryset.none()

    def search_by_local_ip(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(netaddr.IPNetwork(value).cidr)
            return queryset.filter(local_address__address=query)
        except (AddrFormatError, ValueError):
            return queryset.none()


class RoutingPolicyFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = RoutingPolicy
        fields = ['id', 'name', 'description']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(name__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class RoutingPolicyRuleFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = RoutingPolicyRule
        fields = ['id', 'index', 'action', 'description', 'routing_policy_id', 'continue_entry']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(index__icontains=value)
                | Q(action__icontains=value)
                | Q(description__icontains=value)
                | Q(routing_policy_id__icontains=value)
                | Q(continue_entry__icontains=value)
        )
        return queryset.filter(qs_filter)


class BGPPeerGroupFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = BGPPeerGroup
        fields = ['id', 'name', 'description']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(name__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class PrefixListFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = PrefixList
        fields = ['id', 'name', 'description']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(name__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)

class PrefixListRuleFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = PrefixListRule
        #fields = ['index', 'action', 'prefix_custom', 'ge', 'le', 'prefix_list', 'prefix_list_id']
        fields = ['id', 'index', 'action', 'ge', 'le', 'prefix_list', 'prefix_list_id']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(index__icontains=value)
                | Q(action__icontains=value)
                #| Q(prefix_custom__icontains=value)
                | Q(ge__icontains=value)
                | Q(le__icontains=value)
                | Q(prefix_list__icontains=value)
                | Q(prefix_list_id__icontains=value)
        )
        return queryset.filter(qs_filter)
