from rest_framework.serializers import ModelSerializer

from netbox.api import ChoiceField
from dcim.api.nested_serializers import NestedSiteSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer
from extras.api.serializers import TaggedObjectSerializer
from extras.api.customfields import CustomFieldModelSerializer
from netbox_bgp.models import ASN, ASNStatusChoices, BGPSession, SessionStatusChoices


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
