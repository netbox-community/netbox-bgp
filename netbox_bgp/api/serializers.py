from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from ipam.constants import VLANGROUP_SCOPE_TYPES
from rest_framework.serializers import (
    CharField,
    JSONField,
    HyperlinkedIdentityField,
    IntegerField,
    SerializerMethodField,
    ValidationError
)
from rest_framework.relations import PrimaryKeyRelatedField
from netbox.api.fields import ChoiceField, ContentTypeField, SerializedPKRelatedField
from netbox.api.serializers import NetBoxModelSerializer
from ipam.api.serializers import IPAddressSerializer, ASNSerializer, PrefixSerializer, VRFSerializer
from tenancy.api.serializers import TenantSerializer
from dcim.api.serializers import SiteSerializer, DeviceSerializer
from ipam.api.field_serializers import IPNetworkField
from utilities.api import get_serializer_for_model
from virtualization.api.serializers import VirtualMachineSerializer

from netbox_bgp.models import (
    BGPSession,
    RoutingPolicy,
    BGPPeerGroup,
    Community,
    RoutingPolicyRule,
    PrefixList,
    PrefixListRule,
    CommunityList,
    CommunityListRule,
    ASPathList,
    ASPathListRule,
    Redistributing
)

from netbox_bgp.choices import CommunityStatusChoices, SessionStatusChoices, RedistributeSourceChoices


class ASPathListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:aspathlist-detail")

    scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=VLANGROUP_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    scope_id = IntegerField(allow_null=True, required=False, default=None)
    scope = SerializerMethodField(read_only=True)

    class Meta:
        model = ASPathList
        fields = [
            "id",
            "url",
            "name",
            "display",
            "description",
            "scope_type",
            "scope_id",
            "scope",
            "tags",
            "custom_fields",
            "comments",
        ]
        brief_fields = ("id", "url", "display", "name", "description")    

    @extend_schema_field(JSONField(allow_null=True))
    def get_scope(self, obj):
        if obj.scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.scope)
        context = {"request": self.context["request"]}
        return serializer(obj.scope, nested=True, context=context).data

class ASPathListRuleSerializer(NetBoxModelSerializer):
    aspath_list = ASPathListSerializer(nested=True)

    class Meta:
        model = ASPathListRule
        fields = [
            "id",
            "description",
            "tags",
            "custom_fields",
            "display",
            "aspath_list",
            "created",
            "last_updated",
            "index",
            "action",
            "pattern",
            "comments",
        ]
        brief_fields = ("id", "display", "description")


class RoutingPolicySerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:routingpolicy-detail")

    scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=VLANGROUP_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    scope_id = IntegerField(allow_null=True, required=False, default=None)
    scope = SerializerMethodField(read_only=True)

    class Meta:
        model = RoutingPolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "weight",
            "scope_type",
            "scope_id",
            "scope",
            "redistributing",
            "tags",
            "custom_fields",
            "comments",
        )
        brief_fields = ("id", "url", "display", "name", "description")

    @extend_schema_field(JSONField(allow_null=True))
    def get_scope(self, obj):
        if obj.scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.scope)
        context = {"request": self.context["request"]}
        return serializer(obj.scope, nested=True, context=context).data

class PrefixListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:prefixlist-detail")

    scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=VLANGROUP_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    scope_id = IntegerField(allow_null=True, required=False, default=None)
    scope = SerializerMethodField(read_only=True)

    class Meta:
        model = PrefixList
        fields = (
            "id",
            "url",
            "name",
            "display",
            "description",
            "scope_type",
            "scope_id",
            "scope",
            "family",
            "tags",
            "custom_fields",
            "comments",
        )
        brief_fields = ("id", "url", "display", "name", "description")

    @extend_schema_field(JSONField(allow_null=True))
    def get_scope(self, obj):
        if obj.scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.scope)
        context = {"request": self.context["request"]}
        return serializer(obj.scope, nested=True, context=context).data

class BGPPeerGroupSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:bgppeergroup-detail")

    scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=VLANGROUP_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    scope_id = IntegerField(allow_null=True, required=False, default=None)
    scope = SerializerMethodField(read_only=True)
    import_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=RoutingPolicySerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )
    export_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=RoutingPolicySerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )

    class Meta:
        model = BGPPeerGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "scope_type",
            "scope_id",
            "scope",
            "import_policies",
            "export_policies",
            "comments",
            "custom_fields",
        )
        brief_fields = ("id", "url", "display", "name", "description")

    @extend_schema_field(JSONField(allow_null=True))
    def get_scope(self, obj):
        if obj.scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.scope)
        context = {"request": self.context["request"]}
        return serializer(obj.scope, nested=True, context=context).data

class BGPSessionSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:bgpsession-detail")
    status = ChoiceField(choices=SessionStatusChoices, required=False)
    site = SiteSerializer(nested=True, required=False, allow_null=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    virtualmachine = VirtualMachineSerializer(nested=True, required=False, allow_null=True)
    local_address = IPAddressSerializer(nested=True, required=True, allow_null=False)
    remote_address = IPAddressSerializer(nested=True, required=True, allow_null=False)
    local_as = ASNSerializer(nested=True, required=True, allow_null=False)
    remote_as = ASNSerializer(nested=True, required=True, allow_null=False)
    peer_group = BGPPeerGroupSerializer(nested=True, required=False, allow_null=True)
    prefix_list_in = PrefixListSerializer(nested=True, required=False, allow_null=True)
    prefix_list_out = PrefixListSerializer(nested=True, required=False, allow_null=True)
    import_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=RoutingPolicySerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )
    export_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=RoutingPolicySerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )

    class Meta:
        model = BGPSession
        fields = (
            "id",
            "url",
            "tags",
            "custom_fields",
            "display",
            "status",
            "site",
            "tenant",
            "device",
            "virtualmachine",
            "local_address",
            "remote_address",
            "local_as",
            "remote_as",
            "peer_group",
            "import_policies",
            "export_policies",
            "prefix_list_in",
            "prefix_list_out",
            "created",
            "last_updated",
            "name",
            "description",
            "comments",
        )
        brief_fields = ("id", "url", "display", "name", "description")

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if instance is not None:
            if instance.peer_group:
                for pol in instance.peer_group.import_policies.difference(
                    instance.import_policies.all()
                ):
                    ret["import_policies"].append(
                        RoutingPolicySerializer(
                            pol,
                            context={"request": self.context["request"]},
                            nested=True,
                        ).data
                    )
                for pol in instance.peer_group.export_policies.difference(
                    instance.export_policies.all()
                ):
                    ret["export_policies"].append(
                        RoutingPolicySerializer(
                            pol,
                            context={"request": self.context["request"]},
                            nested=True,
                        ).data
                    )
        return ret


class CommunitySerializer(NetBoxModelSerializer):
    status = ChoiceField(choices=CommunityStatusChoices, required=False)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:community-detail")

    class Meta:
        model = Community
        fields = (
            "id",
            "url",
            "tags",
            "custom_fields",
            "display",
            "status",
            "tenant",
            "created",
            "last_updated",
            "description",
            "value",
            "site",
            "role",
            "comments",
        )
        brief_fields = ("id", "url", "display", "value", "description")


class CommunityListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:communitylist-detail")

    scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=VLANGROUP_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    scope_id = IntegerField(allow_null=True, required=False, default=None)
    scope = SerializerMethodField(read_only=True)

    class Meta:
        model = CommunityList
        fields = (
            "id",
            "url",
            "name",
            "display",
            "description",
            "scope_type",
            "scope_id",
            "scope",
            "tags",
            "custom_fields",
            "comments",
        )
        brief_fields = ("id", "url", "display", "name", "description")

    @extend_schema_field(JSONField(allow_null=True))
    def get_scope(self, obj):
        if obj.scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.scope)
        context = {"request": self.context["request"]}
        return serializer(obj.scope, nested=True, context=context).data

class CommunityListRuleSerializer(NetBoxModelSerializer):
    community_list = CommunityListSerializer(nested=True)
    community = CommunitySerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = CommunityListRule
        fields = (
            "id",
            "tags",
            "custom_fields",
            "display",
            "description",
            "community_list",
            "created",
            "last_updated",
            "action",
            "community",
            "comments",
        )
        brief_fields = ("id", "display", "description")


class RoutingPolicyRuleSerializer(NetBoxModelSerializer):
    match_ip_address = SerializedPKRelatedField(
        queryset=PrefixList.objects.all(),
        serializer=PrefixListSerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )
    match_ipv6_address = SerializedPKRelatedField(
        queryset=PrefixList.objects.all(),
        serializer=PrefixListSerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )
    routing_policy = RoutingPolicySerializer(nested=True)

    match_community = SerializedPKRelatedField(
        queryset=Community.objects.all(),
        serializer=CommunitySerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )
    match_community_list = SerializedPKRelatedField(
        queryset=CommunityList.objects.all(),
        serializer=CommunityListSerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )
    match_aspath_list = SerializedPKRelatedField(
        queryset=ASPathList.objects.all(),
        serializer=ASPathListSerializer,
        nested=True,
        required=False,
        allow_null=True,
        many=True,
    )  

    class Meta:
        model = RoutingPolicyRule
        fields = (
            "id",
            "index",
            "display",
            "action",
            "match_ip_address",
            "routing_policy",
            "match_community",
            "match_community_list",
            "match_aspath_list",
            "match_custom",
            "set_actions",
            "match_ipv6_address",
            "description",
            "continue_entry",
            "tags",
            "custom_fields",
            "comments",
        )
        brief_fields = ("id", "display", "description")


class PrefixListRuleSerializer(NetBoxModelSerializer):
    prefix_list = PrefixListSerializer(nested=True)
    prefix = PrefixSerializer(nested=True, required=False, allow_null=True)
    prefix_custom = IPNetworkField(required=False, allow_null=True)

    class Meta:
        model = PrefixListRule
        fields = (
            "id",
            "description",
            "tags",
            "custom_fields",
            "display",
            "prefix_list",
            "created",
            "last_updated",
            "index",
            "action",
            "prefix_custom",
            "ge",
            "le",
            "prefix",
            "comments",
        )
        brief_fields = ("id", "display", "description")


class RedistributingSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:redistributing-detail")
    name = CharField(required=True, allow_null=False)
    scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=VLANGROUP_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    scope_id = IntegerField(allow_null=True, required=False, default=None)
    scope = SerializerMethodField(read_only=True)
    vrf = VRFSerializer(nested=True, required=False, allow_null=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    virtualmachine = VirtualMachineSerializer(nested=True, required=False, allow_null=True)
    redistribute_source = ChoiceField(choices=RedistributeSourceChoices, required=True, allow_null=False)
    redistribute_policy = RoutingPolicySerializer(required=True, allow_null=False)

    class Meta:
        model = Redistributing
        fields = (
            "id",
            "url",
            "tags",
            "custom_fields",
            "display",
            "scope_type",
            "scope_id",
            "scope",
            "vrf",
            "tenant",
            "device",
            "virtualmachine",
            "redistribute_source",
            "redistribute_policy",
            "created",
            "last_updated",
            "name",
            "description",
            "comments",
        )
        brief_fields = ("id", "url", "name", "display", "device", "virtualmachine", "redistribute_source", "redistribute_policy")

    @extend_schema_field(JSONField(allow_null=True))
    def get_scope(self, obj):
        if obj.scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.scope)
        context = {"request": self.context["request"]}
        return serializer(obj.scope, nested=True, context=context).data
