from rest_framework.viewsets import ModelViewSet

from .serializers import ASNSerializer, BGPSessionSerializer, RoutingPolicySerializer
from netbox_bgp.models import ASN, BGPSession, RoutingPolicy
from netbox_bgp.filters import ASNFilterSet, BGPSessionFilterSet, RoutingPolicyFilterSet


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
