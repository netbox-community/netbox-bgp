from rest_framework import routers

from .views import (
    ASNViewSet, BGPSessionViewSet, RoutingPolicyViewSet, BGPPeerGroupViewSet,
    CommunityViewSet
)

router = routers.DefaultRouter()
router.register('asn', ASNViewSet)
router.register('session', BGPSessionViewSet)
router.register('routing-policy', RoutingPolicyViewSet)
router.register('peer-group', BGPPeerGroupViewSet)
router.register('community', CommunityViewSet)


urlpatterns = router.urls
