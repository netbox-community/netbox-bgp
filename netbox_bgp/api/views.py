from rest_framework.viewsets import ModelViewSet

from .serializers import ASNSerializer, BGPSessionSerializer, RoutingPolicySerializer, BGPPeerGroupSerializer
from netbox_bgp.models import ASN, BGPSession, RoutingPolicy, BGPPeerGroup
from netbox_bgp.filters import (
    ASNFilterSet, BGPSessionFilterSet, RoutingPolicyFilterSet, BGPPeerGroupFilterSet
)


class ASNViewSet(ModelViewSet):
    queryset = ASN.objects.all()
    serializer_class = ASNSerializer
    filterset_class = ASNFilterSet


class BGPSessionViewSet(ModelViewSet):
    queryset = BGPSession.objects.all()
    serializer_class = BGPSessionSerializer
    filterset_class = BGPSessionFilterSet


class RoutingPolicyViewSet(ModelViewSet):
    queryset = RoutingPolicy.objects.all()
    serializer_class = RoutingPolicySerializer
    filterset_class = RoutingPolicyFilterSet


class BGPPeerGroupViewSet(ModelViewSet):
    queryset = BGPPeerGroup.objects.all()
    serializer_class = BGPPeerGroupSerializer
    filterset_class = BGPPeerGroupFilterSet
