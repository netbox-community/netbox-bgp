from rest_framework.serializers import Serializer, HyperlinkedIdentityField

from netbox.api import ChoiceField, WritableNestedSerializer
from dcim.api.nested_serializers import NestedSiteSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer

try:
    from extras.api.customfields import CustomFieldModelSerializer
except ImportError:
    from netbox.api.serializers import CustomFieldModelSerializer

from extras.models import Tag
from netbox_bgp.models import ASN, ASNStatusChoices, BGPSession, SessionStatusChoices


class NestedTagSerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(view_name='extras-api:tag-detail')

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'slug', 'color']


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
