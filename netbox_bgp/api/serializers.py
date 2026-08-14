from rest_framework.serializers import HyperlinkedIdentityField, ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from netbox.api.fields import ChoiceField, SerializedPKRelatedField
from netbox.api.serializers import NetBoxModelSerializer
from ipam.api.serializers import IPAddressSerializer, ASNSerializer, PrefixSerializer
from tenancy.api.serializers import TenantSerializer
from dcim.api.serializers import SiteSerializer, DeviceSerializer
from ipam.api.field_serializers import IPNetworkField
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
    ASPathListRule
)

from netbox_bgp.choices import CommunityStatusChoices, SessionStatusChoices


class ASPathListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:aspathlist-detail")

    class Meta:
        model = ASPathList
        fields = [
            "id",
            "url",
            "name",
            "display",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ("id", "url", "display", "name", "description")


class ASPathListRuleSerializer(NetBoxModelSerializer):
    aspath_list = ASPathListSerializer(nested=True)

    class Meta:
        model = ASPathListRule
        fields = [
            "id",
            "description",
            "display",
            "aspath_list",
            "index",
            "action",
            "pattern",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ("id", "display", "description")


class RoutingPolicySerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:routingpolicy-detail")

    class Meta:
        model = RoutingPolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "weight",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "description")


class PrefixListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:prefixlist-detail")

    class Meta:
        model = PrefixList
        fields = (
            "id",
            "url",
            "name",
            "display",
            "description",
            "family",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "description")


class BGPPeerGroupSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:bgppeergroup-detail")

    local_as = ASNSerializer(nested=True, required=False, allow_null=True)
    remote_as = ASNSerializer(nested=True, required=False, allow_null=True)
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
        model = BGPPeerGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "local_as",
            "remote_as",
            "import_policies",
            "export_policies",
            "prefix_list_in",
            "prefix_list_out",
            "extra_attributes",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "description")


class BGPSessionSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:bgpsession-detail")
    status = ChoiceField(choices=SessionStatusChoices, required=False)
    site = SiteSerializer(nested=True, required=False, allow_null=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    virtualmachine = VirtualMachineSerializer(nested=True, required=False, allow_null=True)
    local_address = IPAddressSerializer(nested=True, required=True, allow_null=False)
    remote_address = IPAddressSerializer(nested=True, required=False, allow_null=True)
    remote_prefix = PrefixSerializer(nested=True, required=False, allow_null=True)
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
            "display",
            "status",
            "site",
            "tenant",
            "device",
            "virtualmachine",
            "local_address",
            "remote_address",
            "remote_prefix",
            "local_as",
            "remote_as",
            "remote_as_macro",
            "peer_group",
            "import_policies",
            "export_policies",
            "max_prefixes",
            "prefix_list_in",
            "prefix_list_out",
            "extra_attributes",
            "name",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "description")


class CommunitySerializer(NetBoxModelSerializer):
    status = ChoiceField(choices=CommunityStatusChoices, required=False)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:community-detail")

    class Meta:
        model = Community
        fields = (
            "id",
            "url",
            "display",
            "status",
            "tenant",
            "description",
            "value",
            "site",
            "role",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "value", "description")


class CommunityListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:netbox_bgp-api:communitylist-detail")

    class Meta:
        model = CommunityList
        fields = (
            "id",
            "url",
            "name",
            "display",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "description")


class CommunityListRuleSerializer(NetBoxModelSerializer):
    community_list = CommunityListSerializer(nested=True)
    community = CommunitySerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = CommunityListRule
        fields = (
            "id",
            "display",
            "description",
            "community_list",
            "action",
            "community",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
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
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
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
            "display",
            "prefix_list",
            "index",
            "action",
            "prefix_custom",
            "ge",
            "le",
            "prefix",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "display", "description")

