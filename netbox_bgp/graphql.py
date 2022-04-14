from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import models, filters

class CommunityType(NetBoxObjectType):
    class Meta:
        model = models.Community
        fields = '__all__'
        filterset_class = filters.CommunityFilterSet

class AsnType(NetBoxObjectType):
    class Meta:
        model = models.ASN
        fields = '__all__'
        filterset_class = filters.ASNFilterSet

class BgpSessionType(NetBoxObjectType):
    class Meta:
        model = models.BGPSession
        fields = '__all__'
        filterset_class = filters.BGPSessionFilterSet

class BgpBaseType(NetBoxObjectType):
    class Meta:
        model = models.BGPBase
        fields = '__all__'

class BgpPeerGroupType(NetBoxObjectType):
    class Meta:
        model = models.BGPPeerGroup
        fields = '__all__'
        filterset_class = filters.BGPPeerGroupFilterSet

class RoutingPolicyType(NetBoxObjectType):
    class Meta:
        model = models.RoutingPolicy
        fields = '__all__'
        filterset_class = filters.RoutingPolicyFilterSet

class AsnGroupType(NetBoxObjectType):
    class Meta:
        model = models.ASNGroup
        fields = '__all__'




class BGPQuery(ObjectType):
    community = ObjectField(CommunityType)
    community_list = ObjectListField(CommunityType)

    asn = ObjectField(AsnType)
    asn_list = ObjectListField(AsnType)

    bgpsession = ObjectField(BgpSessionType)
    bgpsession_list = ObjectListField(BgpSessionType)

    bgpbase = ObjectField(BgpBaseType)
    bgpbase_list = ObjectListField(BgpBaseType)

    bgppeergroup = ObjectField(BgpPeerGroupType)
    bgppeergroup_list = ObjectListField(BgpPeerGroupType)

    routingpolicy = ObjectField(RoutingPolicyType)
    routingpolicy_list = ObjectListField(RoutingPolicyType)

    asngroup = ObjectField(AsnGroupType)
    asngroup_list = ObjectListField(AsnGroupType)

schema = BGPQuery