from rest_framework.viewsets import ModelViewSet

from .serializers import ASNSerializer, BGPSessionSerializer
from netbox_bgp.models import ASN, BGPSession
from netbox_bgp.filters import ASNFilterSet, BGPSessionFilterSet


class ASNViewSet(ModelViewSet):
    queryset = ASN.objects.all()
    serializer_class = ASNSerializer
    filterset_class = ASNFilterSet


class BGPSessionViewSet(ModelViewSet):
    queryset = BGPSession.objects.all()
    serializer_class = BGPSessionSerializer
    filterset_class = BGPSessionFilterSet
