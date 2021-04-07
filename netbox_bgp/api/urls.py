from rest_framework import routers

from .views import ASNViewSet, BGPSessionViewSet

router = routers.DefaultRouter()
router.register('asn', ASNViewSet)
router.register('session', BGPSessionViewSet)

urlpatterns = router.urls
