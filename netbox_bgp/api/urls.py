from rest_framework import routers

from .views import (
    BGPSessionViewSet, RoutingPolicyViewSet, BGPPeerGroupViewSet, CommunityViewSet,
    PrefixListViewSet, PrefixListRuleViewSet, RoutingPolicyRuleViewSet,
    CommunityListViewSet, CommunityListRuleViewSet
)

router = routers.DefaultRouter()
router.register('session', BGPSessionViewSet, 'session')
router.register('bgpsession', BGPSessionViewSet, 'bgpsession')
router.register('routing-policy', RoutingPolicyViewSet)
router.register('routing-policy-rule', RoutingPolicyRuleViewSet)
router.register('peer-group', BGPPeerGroupViewSet, 'peergroup')
router.register('bgppeergroup', BGPPeerGroupViewSet, 'bgppeergroup')
router.register('community', CommunityViewSet)
router.register('prefix-list', PrefixListViewSet)
router.register('prefix-list-rule', PrefixListRuleViewSet)
router.register('community-list', CommunityListViewSet)
router.register('community-list-rule', CommunityListRuleViewSet)

urlpatterns = router.urls
