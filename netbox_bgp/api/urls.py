from netbox.api.routers import NetBoxRouter

from .views import (
    BGPSessionViewSet, RoutingPolicyViewSet, BGPPeerGroupViewSet, CommunityViewSet,
    PrefixListViewSet, PrefixListRuleViewSet, RoutingPolicyRuleViewSet,
    CommunityListViewSet, CommunityListRuleViewSet, RootView, ASPathListViewSet, ASPathListRuleViewSet
)


router = NetBoxRouter()
router.APIRootView = RootView
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
router.register('aspath-list', ASPathListViewSet)
router.register('aspath-list-rule', ASPathListRuleViewSet)

urlpatterns = router.urls
