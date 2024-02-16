from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from .models import (
    BGPSession, Community, RoutingPolicy,
    BGPPeerGroup, RoutingPolicyRule, PrefixList,
    PrefixListRule, CommunityList, CommunityListRule
)

from . import views

urlpatterns = [
    # Community
    path('community/', views.CommunityListView.as_view(), name='community_list'),
    path('community/add/', views.CommunityEditView.as_view(), name='community_add'),
    path('community/import/', views.CommunityBulkImportView.as_view(), name='community_import'),
    path('community/edit/', views.CommunityBulkEditView.as_view(), name='community_bulk_edit'),
    path('community/delete/', views.CommunityBulkDeleteView.as_view(), name='community_bulk_delete'),
    path('community/<int:pk>/', views.CommunityView.as_view(), name='community'),
    path('community/<int:pk>/edit/', views.CommunityEditView.as_view(), name='community_edit'),
    path('community/<int:pk>/delete/', views.CommunityDeleteView.as_view(), name='community_delete'),
    path('community/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='community_changelog', kwargs={'model': Community}),
    # Community Lists
    path('community-list/', views.CommunityListListView.as_view(), name='communitylist_list'),
    path('community-list/add/', views.CommunityListEditView.as_view(), name='communitylist_add'),
    path('community-list/delete/', views.CommunityListBulkDeleteView.as_view(), name='communitylist_bulk_delete'),
    path('community-list/<int:pk>/', views.CommListView.as_view(), name='communitylist'),
    path('community-list/<int:pk>/edit/', views.CommunityListEditView.as_view(), name='communitylist_edit'),
    path('community-list/<int:pk>/delete/', views.CommunityListDeleteView.as_view(), name='communitylist_delete'),
    path('community-list/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='communitylist_changelog', kwargs={'model': CommunityList}),
    # Community List Rules
    path('community-list-rule/', views.CommunityListRuleListView.as_view(), name='communitylistrule_list'),
    path('community-list-rule/add/', views.CommunityListRuleEditView.as_view(), name='communitylistrule_add'),
    path('community-list-rule/<int:pk>/', views.CommunityListRuleView.as_view(), name='communitylistrule'),
    path('community-list-rule/<int:pk>/edit/', views.CommunityListRuleEditView.as_view(), name='communitylistrule_edit'),
    path('community-list-rule/<int:pk>/delete/', views.CommunityListRuleDeleteView.as_view(), name='communitylistrule_delete'),
    path('community-list-rule/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='communitylistrule_changelog', kwargs={'model': CommunityListRule}),    
    # Sessions
    path('session/', views.BGPSessionListView.as_view(), name='bgpsession_list'),
    path('session/add/', views.BGPSessionAddView.as_view(), name='bgpsession_add'),
    path('session/import/', views.BGPSessionBulkImportView.as_view(), name='bgpsession_import'),
    path('session/edit/', views.BGPSessionBulkEditView.as_view(), name='bgpsession_bulk_edit'),
    path('session/delete/', views.BGPSessionBulkDeleteView.as_view(), name='bgpsession_bulk_delete'),
    path('session/<int:pk>/', views.BGPSessionView.as_view(), name='bgpsession'),
    path('session/<int:pk>/edit/', views.BGPSessionEditView.as_view(), name='bgpsession_edit'),
    path('session/<int:pk>/delete/', views.BGPSessionDeleteView.as_view(), name='bgpsession_delete'),
    path('session/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='bgpsession_changelog', kwargs={'model': BGPSession}),
    # Routing Policies
    path('routing-policy/', views.RoutingPolicyListView.as_view(), name='routingpolicy_list'),
    path('routing-policy/add/', views.RoutingPolicyEditView.as_view(), name='routingpolicy_add'),
    path('routing-policy/delete/', views.RoutingPolicyBulkDeleteView.as_view(), name='routingpolicy_bulk_delete'),
    path('routing-policy/<int:pk>/', views.RoutingPolicyView.as_view(), name='routingpolicy'),
    path('routing-policy/<int:pk>/edit/', views.RoutingPolicyEditView.as_view(), name='routingpolicy_edit'),
    path('routing-policy/<int:pk>/delete/', views.RoutingPolicyDeleteView.as_view(), name='routingpolicy_delete'),
    path('routing-policy/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='routingpolicy_changelog', kwargs={'model': RoutingPolicy}),
    # Peer Groups
    path('peer-group/', views.BGPPeerGroupListView.as_view(), name='bgppeergroup_list'),
    path('peer-group/add/', views.BGPPeerGroupEditView.as_view(), name='bgppeergroup_add'),
    path('peer-group/delete/', views.BGPPeerGroupBulkDeleteView.as_view(), name='bgppeergroup_bulk_delete'),
    path('peer-group/<int:pk>/', views.BGPPeerGroupView.as_view(), name='bgppeergroup'),
    path('peer-group/<int:pk>/edit/', views.BGPPeerGroupEditView.as_view(), name='bgppeergroup_edit'),
    path('peer-group/<int:pk>/delete/', views.BGPPeerGroupDeleteView.as_view(), name='bgppeergroup_delete'),
    path('peer-group/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='bgppeergroup_changelog', kwargs={'model': BGPPeerGroup}),
    # Routing Policy Rules
    path('routing-policy-rule/', views.RoutingPolicyRuleListView.as_view(), name='routingpolicyrule_list'),
    path('routing-policy-rule/add/', views.RoutingPolicyRuleEditView.as_view(), name='routingpolicyrule_add'),
    path('routing-policy-rule/<int:pk>/', views.RoutingPolicyRuleView.as_view(), name='routingpolicyrule'),
    path('routing-policy-rule/<int:pk>/edit/', views.RoutingPolicyRuleEditView.as_view(), name='routingpolicyrule_edit'),
    path('routing-policy-rule/<int:pk>/delete/', views.RoutingPolicyRuleDeleteView.as_view(), name='routingpolicyrule_delete'),
    path('routing-policy-rule/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='routingpolicyrule_changelog', kwargs={'model': RoutingPolicyRule}),
    # Prefix Lists
    path('prefix-list/', views.PrefixListListView.as_view(), name='prefixlist_list'),
    path('prefix-list/add/', views.PrefixListEditView.as_view(), name='prefixlist_add'),
    path('prefix-list/delete/', views.PrefixListBulkDeleteView.as_view(), name='prefixlist_bulk_delete'),
    path('prefix-list/<int:pk>/', views.PrefixListView.as_view(), name='prefixlist'),
    path('prefix-list/<int:pk>/edit/', views.PrefixListEditView.as_view(), name='prefixlist_edit'),
    path('prefix-list/<int:pk>/delete/', views.PrefixListDeleteView.as_view(), name='prefixlist_delete'),
    path('prefix-list/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='prefixlist_changelog', kwargs={'model': PrefixList}),
    # Prefix List Rules
    path('prefix-list-rule/', views.PrefixListRuleListView.as_view(), name='prefixlistrule_list'),
    path('prefix-list-rule/add/', views.PrefixListRuleEditView.as_view(), name='prefixlistrule_add'),
    path('prefix-list-rule/<int:pk>/', views.PrefixListRuleView.as_view(), name='prefixlistrule'),
    path('prefix-list-rule/<int:pk>/edit/', views.PrefixListRuleEditView.as_view(), name='prefixlistrule_edit'),
    path('prefix-list-rule/<int:pk>/delete/', views.PrefixListRuleDeleteView.as_view(), name='prefixlistrule_delete'),
    path('prefix-list-rule/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='prefixlistrule_changelog', kwargs={'model': PrefixListRule}),
]
