from rest_framework.serializers import HyperlinkedIdentityField, ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from netbox.api.fields import ChoiceField, SerializedPKRelatedField

from netbox.api.serializers import NetBoxModelSerializer
from ipam.api.serializers import IPAddressSerializer, ASNSerializer, PrefixSerializer
from tenancy.api.serializers import TenantSerializer
from dcim.api.serializers import SiteSerializer, DeviceSerializer

from ipam.api.field_serializers import IPNetworkField

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
)

from netbox_bgp.choices import CommunityStatusChoices, SessionStatusChoices


class RoutingPolicySerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins:netbox_bgp:routingpolicy")

    class Meta:
        model = RoutingPolicy
        fields = [
            "id",
            "url",
            "display",
            "name",
            "description",
            "tags",
            "custom_fields",
            "comments",
        ]
        brief_fields = ("id", "url", "display", "name", "description")


class PrefixListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins:netbox_bgp:prefixlist")

    class Meta:
        model = PrefixList
        fields = [
            "id",
            "url",
            "name",
            "display",
            "description",
            "family",
            "tags",
            "custom_fields",
            "comments",
        ]
        brief_fields = ("id", "url", "display", "name", "description")


class BGPPeerGroupSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins:netbox_bgp:bgppeergroup")

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
        fields = [
            "id",
            "url",
            "display",
            "name",
            "description",
            "import_policies",
            "export_policies",
            "comments",
        ]
        brief_fields = ("id", "url", "display", "name", "description")


class BGPSessionSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins:netbox_bgp:bgpsession")
    status = ChoiceField(choices=SessionStatusChoices, required=False)
    site = SiteSerializer(nested=True, required=False, allow_null=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
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
        fields = [
            "id",
            "url",
            "tags",
            "custom_fields",
            "display",
            "status",
            "site",
            "tenant",
            "device",
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
        ]
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
    url = HyperlinkedIdentityField(view_name="plugins:netbox_bgp:community")

    class Meta:
        model = Community
        fields = [
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
        ]
        brief_fields = ("id", "url", "display", "value", "description")


class CommunityListSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins:netbox_bgp:communitylist")

    class Meta:
        model = CommunityList
        fields = [
            "id",
            "url",
            "name",
            "display",
            "description",
            "tags",
            "custom_fields",
            "comments",
        ]
        brief_fields = ("id", "url", "display", "name", "description")


class CommunityListRuleSerializer(NetBoxModelSerializer):
    community_list = CommunityListSerializer(nested=True)
    community = CommunitySerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = CommunityListRule
        fields = [
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
        ]
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

    class Meta:
        model = RoutingPolicyRule
        fields = [
            "id",
            "index",
            "display",
            "action",
            "match_ip_address",
            "routing_policy",
            "match_community",
            "match_community_list",
            "match_custom",
            "set_actions",
            "match_ipv6_address",
            "description",
            "tags",
            "custom_fields",
            "comments",
        ]
        brief_fields = ("id", "display", "description")


class PrefixListRuleSerializer(NetBoxModelSerializer):
    prefix_list = PrefixListSerializer(nested=True)
    prefix = PrefixSerializer(nested=True, required=False, allow_null=True)
    prefix_custom = IPNetworkField(required=False, allow_null=True)

    class Meta:
        model = PrefixListRule
        fields = [
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
        ]
        brief_fields = ("id", "display", "description")
