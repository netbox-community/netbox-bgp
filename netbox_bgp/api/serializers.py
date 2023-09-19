from rest_framework.serializers import HyperlinkedIdentityField, ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from netbox.api.fields import ChoiceField
from netbox.api.serializers.nested import WritableNestedSerializer

from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.nested_serializers import NestedSiteSerializer, NestedDeviceSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer
from ipam.api.nested_serializers import NestedIPAddressSerializer, NestedASNSerializer, NestedPrefixSerializer


from netbox_bgp.models import (
    BGPSession, RoutingPolicy, BGPPeerGroup,
    Community, RoutingPolicyRule, PrefixList, PrefixListRule,
)

from netbox_bgp.choices import CommunityStatusChoices, SessionStatusChoices


class SerializedPKRelatedField(PrimaryKeyRelatedField):
    def __init__(self, serializer, **kwargs):
        self.serializer = serializer
        self.pk_field = kwargs.pop('pk_field', None)
        super().__init__(**kwargs)

    def to_representation(self, value):
        return self.serializer(value, context={'request': self.context['request']}).data


class RoutingPolicySerializer(NetBoxModelSerializer):
    class Meta:
        model = RoutingPolicy        
        fields = '__all__'


class NestedRoutingPolicySerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(view_name='plugins:netbox_bgp:routingpolicy')

    class Meta:
        model = RoutingPolicy
        fields = ['id', 'url', 'name', 'display', 'description']        
        validators = []

class BGPPeerGroupSerializer(NetBoxModelSerializer):
    import_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        allow_null=True,
        many=True
    )
    export_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        allow_null=True,
        many=True
    )

    class Meta:
        model = BGPPeerGroup
        fields = '__all__'


class NestedBGPPeerGroupSerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(view_name='plugins:netbox_bgp:bgppeergroup')

    class Meta:
        model = BGPPeerGroup
        fields = ['id', 'url', 'name', 'description']
        validators = []


class BGPSessionSerializer(NetBoxModelSerializer):
    status = ChoiceField(choices=SessionStatusChoices, required=False)
    site = NestedSiteSerializer(required=False, allow_null=True)
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    device = NestedDeviceSerializer(required=False, allow_null=True)
    local_address = NestedIPAddressSerializer(required=True, allow_null=False)
    remote_address = NestedIPAddressSerializer(required=True, allow_null=False)
    local_as = NestedASNSerializer(required=True, allow_null=False)
    remote_as = NestedASNSerializer(required=True, allow_null=False)
    peer_group = NestedBGPPeerGroupSerializer(required=False, allow_null=True)
    import_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        allow_null=True,
        many=True
    )
    export_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        allow_null=True,
        many=True
    )

    class Meta:
        model = BGPSession
        fields = [
            'id', 'tags', 'custom_fields',
            'display', 'status', 'site', 'tenant',
            'device', 'local_address', 'remote_address',
            'local_as', 'remote_as', 'peer_group', 'import_policies',
            'export_policies', 'created', 'last_updated',
            'name', 'description'
            ]


    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if instance is not None:
            if instance.peer_group:
                for pol in instance.peer_group.import_policies.difference(instance.import_policies.all()):
                    ret['import_policies'].append(
                        NestedRoutingPolicySerializer(pol, context={'request': self.context['request']}).data
                    )
                for pol in instance.peer_group.export_policies.difference(instance.export_policies.all()):
                    ret['export_policies'].append(
                        NestedRoutingPolicySerializer(pol, context={'request': self.context['request']}).data
                    )
        return ret


class NestedBGPSessionSerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(view_name='plugins:netbox_bgp:bgpsession')

    class Meta:
        model = BGPSession
        fields = ['id', 'url', 'name', 'description']
        validators = []


class CommunitySerializer(NetBoxModelSerializer):
    status = ChoiceField(choices=CommunityStatusChoices, required=False)
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = Community
        fields = [
            'id', 'tags', 'custom_fields', 'display',
            'status', 'tenant', 'created', 'last_updated',
            'description',
            'value', 'site', 'role'
        ]

class NestedCommunitySerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(view_name='plugins:netbox_bgp:community')

    class Meta:
        model = Community
        fields = [
            'id', 'url', 'display', 'value'
        ]


class NestedPrefixListSerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(view_name='plugins:netbox_bgp:prefixlist')

    class Meta:
        model = PrefixList
        fields = ['id', 'url', 'display', 'name']

class PrefixListSerializer(NetBoxModelSerializer):
    class Meta:
        model = PrefixList
        fields = '__all__'

class RoutingPolicyRuleSerializer(NetBoxModelSerializer):
    match_ip_address = SerializedPKRelatedField(
        queryset=PrefixList.objects.all(),
        serializer=NestedPrefixListSerializer,
        required=False,
        allow_null=True,
        many=True
    )
    routing_policy = NestedRoutingPolicySerializer()
    match_community = SerializedPKRelatedField(
        queryset=Community.objects.all(),
        serializer=NestedCommunitySerializer,
        required=False,
        allow_null=True,
        many=True
    )
    

    class Meta:
        model = RoutingPolicyRule
        fields = '__all__'

class PrefixListRuleSerializer(NetBoxModelSerializer):
    prefix_list = NestedPrefixListSerializer()  
    prefix = NestedPrefixSerializer(required=False, allow_null=True)

    class Meta:
        model = PrefixListRule
        fields = [
            'id', 'tags', 'custom_fields', 'display',
            'prefix_list', 'created', 'last_updated',
            'index', 'action',
            'prefix_custom', 'ge', 'le', 'prefix'
        ]
