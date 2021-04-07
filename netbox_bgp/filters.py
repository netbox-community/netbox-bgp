import django_filters
from django.db.models import Q

from utilities.filters import TagFilter

from .models import ASN, Community, BGPSession


class ASNFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()

    class Meta:
        model = ASN
        fields = ['number', 'description', 'status', 'tenant', 'site']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(number__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class CommunityFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()

    class Meta:
        model = Community
        fields = ['value', 'description', 'status', 'tenant']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(value__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class BGPSessionFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()
    remote_as = django_filters.ModelMultipleChoiceFilter(
        queryset=ASN.objects.all(),
    )

    class Meta:
        model = BGPSession
        fields = ['description', 'status', 'tenant']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(remote_as__number__icontains=value)
            | Q(local_as__number__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
