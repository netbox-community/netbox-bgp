from rest_framework.serializers import Serializer

from netbox.api import ChoiceField
from dcim.api.nested_serializers import NestedSiteSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer
from extras.api.nested_serializers import NestedTagSerializer

try:
    from extras.api.customfields import CustomFieldModelSerializer
except ImportError:
    from netbox.api.serializers import CustomFieldModelSerializer

from netbox_bgp.models import ASN, ASNStatusChoices, BGPSession, SessionStatusChoices, RoutingPolicy


class TaggedObjectSerializer(Serializer):
    tags = NestedTagSerializer(many=True, required=False)

    def create(self, validated_data):
        tags = validated_data.pop('tags', None)
        instance = super().create(validated_data)

        if tags is not None:
            return self._save_tags(instance, tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        # Cache tags on instance for change logging
        instance._tags = tags or []

        instance = super().update(instance, validated_data)
        if tags is not None:
            return self._save_tags(instance, tags)
        return instance

    def _save_tags(self, instance, tags):
        if tags:
            instance.tags.set(*[t.name for t in tags])
        else:
            instance.tags.clear()
        return instance


class ASNSerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    status = ChoiceField(choices=ASNStatusChoices, required=False)
    site = NestedSiteSerializer(required=False, allow_null=True)
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = ASN
        fields = ['number', 'id', 'status', 'description', 'site', 'tenant', 'tags']


class BGPSessionSerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    status = ChoiceField(choices=SessionStatusChoices, required=False)
    site = NestedSiteSerializer(required=False, allow_null=True)
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = BGPSession
        fields = '__all__'


class RoutingPolicySerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    class Meta:
        model = RoutingPolicy
        fields = '__all__'
