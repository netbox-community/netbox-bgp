from rest_framework import routers

from .views import ASNViewSet, BGPSessionViewSet, RoutingPolicyViewSet

router = routers.DefaultRouter()
router.register('asn', ASNViewSet)
router.register('session', BGPSessionViewSet),
router.register('routing-policy', RoutingPolicyViewSet)


urlpatterns = router.urls
