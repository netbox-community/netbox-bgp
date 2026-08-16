from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from utilities.views import register_model_view, ViewTab
from netbox.views import generic
from extras.ui.panels import CustomFieldsPanel, TagsPanel
from netbox.ui import layout
# Aliased: this module already imports a different AddObject from netbox.object_actions,
# which supplies list-view buttons rather than panel actions.
from netbox.ui import actions as panel_actions
from netbox.ui.panels import (
    CommentsPanel,
    ContextTablePanel,
    JSONPanel,
    PluginContentPanel,
    TemplatePanel,
)
from ipam.models import ASN
from virtualization.models import VirtualMachine

from .models import (
    Community, BGPSession, RoutingPolicy,
    BGPPeerGroup, RoutingPolicyRule, PrefixList,
    PrefixListRule, CommunityList, CommunityListRule,
    ASPathList, ASPathListRule
)

from . import filtersets, forms, tables
from .ui import panels
from netbox.object_actions import AddObject, BulkDelete, BulkExport, BulkImport


# Community

@register_model_view(Community, "list", path="", detail=False)
class CommunityListView(generic.ObjectListView):
    queryset = Community.objects.all()
    filterset = filtersets.CommunityFilterSet
    filterset_form = forms.CommunityFilterForm
    table = tables.CommunityTable

@register_model_view(Community)
class CommunityView(generic.ObjectView):
    queryset = Community.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            panels.CommunityPanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
            PluginContentPanel('left_page'),
        ],
        right_panels=[
            PluginContentPanel('right_page'),
        ],
        bottom_panels=[
            PluginContentPanel('full_width_page'),
        ],
    )

@register_model_view(Community, "add", detail=False)
@register_model_view(Community, "edit")
class CommunityEditView(generic.ObjectEditView):
    queryset = Community.objects.all()
    form = forms.CommunityForm

@register_model_view(Community, "bulk_delete", path="delete", detail=False)
class CommunityBulkDeleteView(generic.BulkDeleteView):
    queryset = Community.objects.all()
    table = tables.CommunityTable

@register_model_view(Community, "bulk_edit", path="edit", detail=False)
class CommunityBulkEditView(generic.BulkEditView):
    queryset = Community.objects.all()
    filterset = filtersets.CommunityFilterSet
    table = tables.CommunityTable
    form = forms.CommunityBulkEditForm

@register_model_view(Community, "delete")
class CommunityDeleteView(generic.ObjectDeleteView):
    queryset = Community.objects.all()
    default_return_url = 'plugins:netbox_bgp:community_list'

@register_model_view(Community, "bulk_import", path="import", detail=False)
class CommunityBulkImportView(generic.BulkImportView):
    queryset = Community.objects.all()
    model_form = forms.CommunityImportForm


# Community List

@register_model_view(CommunityList, "list", path="", detail=False)
class CommunityListListView(generic.ObjectListView):
    queryset = CommunityList.objects.all()
    filterset = filtersets.CommunityListFilterSet
    filterset_form = forms.CommunityListFilterForm
    table = tables.CommunityListTable

@register_model_view(CommunityList, "add", detail=False)
@register_model_view(CommunityList, "edit")
class CommunityListEditView(generic.ObjectEditView):
    queryset = CommunityList.objects.all()
    form = forms.CommunityListForm

@register_model_view(CommunityList, "bulk_delete", path="delete", detail=False)
class CommunityListBulkDeleteView(generic.BulkDeleteView):
    queryset = CommunityList.objects.all()
    table = tables.CommunityListTable

@register_model_view(CommunityList, "bulk_edit", path="edit", detail=False)
class CommunityListBulkEditView(generic.BulkEditView):
    queryset = CommunityList.objects.all()
    filterset = filtersets.CommunityListFilterSet
    table = tables.CommunityListTable
    form = forms.CommunityListBulkEditForm

@register_model_view(CommunityList)
class CommListView(generic.ObjectView):
    queryset = CommunityList.objects.all()
    template_name = 'generic/object.html'
    layout = layout.Layout(
        layout.Row(
            layout.Column(
                panels.CommunityListPanel(),
                CustomFieldsPanel(),
                TagsPanel(),
                CommentsPanel(),
                PluginContentPanel('left_page'),
            ),
            layout.Column(
                ContextTablePanel(
                    'rprules_table', title=_('Related Routing Policy Rules')
                ),
                PluginContentPanel('right_page'),
            ),
        ),
        layout.Row(
            layout.Column(
                ContextTablePanel(
                    'rules_table',
                    title=_('Rules'),
                    actions=[
                        panel_actions.AddObject(
                            'netbox_bgp.communitylistrule',
                            url_params={'community_list': lambda ctx: ctx['object'].pk},
                            label=_('Rule'),
                        ),
                    ],
                ),
                PluginContentPanel('full_width_page'),
            ),
        ),
    )

    def get_extra_context(self, request, instance):
        rprules_table = tables.RoutingPolicyRuleTable(instance.cmrules.all())
        rprules_table.configure(request)
        rules_table = tables.CommunityListRuleTable(instance.commlistrules.all())
        rules_table.configure(request)
        return {
            'rules_table': rules_table,
            'rprules_table': rprules_table
        }

@register_model_view(CommunityList, "delete")
class CommunityListDeleteView(generic.ObjectDeleteView):
    queryset = CommunityList.objects.all()
    default_return_url = 'plugins:netbox_bgp:communitylist_list'

@register_model_view(CommunityList, "bulk_import", path="import", detail=False)
class CommunityListBulkImportView(generic.BulkImportView):
    queryset = CommunityList.objects.all()
    model_form = forms.CommunityListImportForm


# Community List Rule

@register_model_view(CommunityListRule, "list", path="", detail=False)
class CommunityListRuleListView(generic.ObjectListView):
    queryset = CommunityListRule.objects.all()
    filterset = filtersets.CommunityListRuleFilterSet
    # filterset_form = RoutingPolicyRuleFilterForm
    table = tables.CommunityListRuleTable
    actions = (AddObject, BulkDelete)

@register_model_view(CommunityListRule, "add", detail=False)
@register_model_view(CommunityListRule, "edit")
class CommunityListRuleEditView(generic.ObjectEditView):
    queryset = CommunityListRule.objects.all()
    form = forms.CommunityListRuleForm

@register_model_view(CommunityListRule, "bulk_delete", path="delete", detail=False)
class CommunityListRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = CommunityListRule.objects.all()
    table = tables.CommunityListRuleTable

@register_model_view(CommunityListRule, "delete")
class CommunityListRuleDeleteView(generic.ObjectDeleteView):
    queryset = CommunityListRule.objects.all()
    default_return_url = 'plugins:netbox_bgp:communitylistrule_list'

@register_model_view(CommunityListRule)
class CommunityListRuleView(generic.ObjectView):
    queryset = CommunityListRule.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            panels.CommunityListRulePanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
            PluginContentPanel('left_page'),
        ],
        right_panels=[
            PluginContentPanel('right_page'),
        ],
        bottom_panels=[
            PluginContentPanel('full_width_page'),
        ],
    )


# Session

@register_model_view(BGPSession, "list", path="", detail=False)
class BGPSessionListView(generic.ObjectListView):
    queryset = BGPSession.objects.all()
    filterset = filtersets.BGPSessionFilterSet
    filterset_form = forms.BGPSessionFilterForm
    table = tables.BGPSessionTable

@register_model_view(BGPSession, "edit")
class BGPSessionEditView(generic.ObjectEditView):
    queryset = BGPSession.objects.all()
    form = forms.BGPSessionForm

@register_model_view(BGPSession, "add", detail=False)
class BGPSessionAddView(generic.ObjectEditView):
    queryset = BGPSession.objects.all()
    form = forms.BGPSessionAddForm

@register_model_view(BGPSession, "bulk_import", path="import", detail=False)
class BGPSessionBulkImportView(generic.BulkImportView):
    queryset = BGPSession.objects.all()
    model_form = forms.BGPSessionImportForm

@register_model_view(BGPSession, "bulk_edit", path="edit", detail=False)
class BGPSessionBulkEditView(generic.BulkEditView):
    queryset = BGPSession.objects.all()
    filterset = filtersets.BGPSessionFilterSet
    table = tables.BGPSessionTable
    form = forms.BGPSessionBulkEditForm

@register_model_view(BGPSession, "bulk_delete", path="delete", detail=False)
class BGPSessionBulkDeleteView(generic.BulkDeleteView):
    queryset = BGPSession.objects.all()
    table = tables.BGPSessionTable

@register_model_view(BGPSession)
class BGPSessionView(generic.ObjectView):
    queryset = BGPSession.objects.all()
    template_name = 'generic/object.html'
    layout = layout.Layout(
        layout.Row(
            layout.Column(
                panels.BGPSessionPanel(),
                CustomFieldsPanel(),
                TagsPanel(),
                JSONPanel('extra_attributes', title=_('Extra Attributes')),
                CommentsPanel(),
                PluginContentPanel('left_page'),
            ),
            layout.Column(
                ContextTablePanel('import_policies_table', title=_('Import Policies')),
                ContextTablePanel('export_policies_table', title=_('Export Policies')),
                PluginContentPanel('right_page'),
            ),
        ),
        layout.Row(
            layout.Column(
                PluginContentPanel('full_width_page'),
            ),
        ),
    )

    def get_extra_context(self, request, instance):
        import_policies_qs = instance.import_policies.all()
        if not import_policies_qs and instance.peer_group:
            import_policies_qs = instance.peer_group.import_policies.all()
        export_policies_qs = instance.export_policies.all()
        if not export_policies_qs and instance.peer_group:
            export_policies_qs = instance.peer_group.export_policies.all()

        import_policies_table = tables.RoutingPolicyTable(
            import_policies_qs,
            orderable=False
        )
        import_policies_table.configure(request)
        export_policies_table = tables.RoutingPolicyTable(
            export_policies_qs,
            orderable=False
        )
        export_policies_table.configure(request)

        return {
            'import_policies_table': import_policies_table,
            'export_policies_table': export_policies_table
        }

@register_model_view(BGPSession, "delete")
class BGPSessionDeleteView(generic.ObjectDeleteView):
    queryset = BGPSession.objects.all()
    default_return_url = 'plugins:netbox_bgp:bgpsession_list'


# Routing Policy

@register_model_view(RoutingPolicy, "list", path="", detail=False)
class RoutingPolicyListView(generic.ObjectListView):
    queryset = RoutingPolicy.objects.all()
    filterset = filtersets.RoutingPolicyFilterSet
    filterset_form = forms.RoutingPolicyFilterForm
    table = tables.RoutingPolicyTable

@register_model_view(RoutingPolicy, "add", detail=False)
@register_model_view(RoutingPolicy, "edit")
class RoutingPolicyEditView(generic.ObjectEditView):
    queryset = RoutingPolicy.objects.all()
    form = forms.RoutingPolicyForm

@register_model_view(RoutingPolicy, "bulk_delete", path="delete", detail=False)
class RoutingPolicyBulkDeleteView(generic.BulkDeleteView):
    queryset = RoutingPolicy.objects.all()
    table = tables.RoutingPolicyTable

@register_model_view(RoutingPolicy, "bulk_edit", path="edit", detail=False)
class RoutingPolicyBulkEditView(generic.BulkEditView):
    queryset = RoutingPolicy.objects.all()
    filterset = filtersets.RoutingPolicyFilterSet
    table = tables.RoutingPolicyTable
    form = forms.RoutingPolicyBulkEditForm

@register_model_view(RoutingPolicy)
class RoutingPolicyView(generic.ObjectView):
    queryset = RoutingPolicy.objects.all()
    template_name = 'generic/object.html'
    layout = layout.Layout(
        layout.Row(
            layout.Column(
                panels.RoutingPolicyPanel(),
                CustomFieldsPanel(),
                TagsPanel(),
                CommentsPanel(),
                PluginContentPanel('left_page'),
            ),
            layout.Column(
                ContextTablePanel(
                    'related_session_table', title=_('Related BGP Sessions')
                ),
                PluginContentPanel('right_page'),
            ),
        ),
        layout.Row(
            layout.Column(
                ContextTablePanel(
                    'rules_table',
                    title=_('Rules'),
                    actions=[
                        panel_actions.AddObject(
                            'netbox_bgp.routingpolicyrule',
                            url_params={'routing_policy': lambda ctx: ctx['object'].pk},
                            label=_('Rule'),
                        ),
                    ],
                ),
                PluginContentPanel('full_width_page'),
            ),
        ),
    )

    def get_extra_context(self, request, instance):
        sess = BGPSession.objects.filter(
            Q(import_policies=instance)
            | Q(export_policies=instance)
            | Q(peer_group__in=instance.group_import_policies.all())
            | Q(peer_group__in=instance.group_export_policies.all())
        )
        sess = sess.distinct()
        sess_table = tables.BGPSessionTable(sess)
        sess_table.configure(request)
        rules_table = tables.RoutingPolicyRuleTable(instance.rules.all())
        rules_table.configure(request)
        return {
            'rules_table': rules_table,
            'related_session_table': sess_table
        }

@register_model_view(RoutingPolicy, "delete")
class RoutingPolicyDeleteView(generic.ObjectDeleteView):
    queryset = RoutingPolicy.objects.all()
    default_return_url = 'plugins:netbox_bgp:routingpolicy_list'

@register_model_view(RoutingPolicy, "bulk_import", path="import", detail=False)
class RoutingPolicyBulkImportView(generic.BulkImportView):
    queryset = RoutingPolicy.objects.all()
    model_form = forms.RoutingPolicyImportForm


# Routing Policy Rule

@register_model_view(RoutingPolicyRule, "list", path="", detail=False)
class RoutingPolicyRuleListView(generic.ObjectListView):
    queryset = RoutingPolicyRule.objects.all()
    filterset = filtersets.RoutingPolicyRuleFilterSet
    # filterset_form = RoutingPolicyRuleFilterForm
    table = tables.RoutingPolicyRuleTable
    actions = (AddObject, BulkImport, BulkExport, BulkDelete)

@register_model_view(RoutingPolicyRule, "add", detail=False)
@register_model_view(RoutingPolicyRule, "edit")
class RoutingPolicyRuleEditView(generic.ObjectEditView):
    queryset = RoutingPolicyRule.objects.all()
    form = forms.RoutingPolicyRuleForm

@register_model_view(RoutingPolicyRule, "delete")
class RoutingPolicyRuleDeleteView(generic.ObjectDeleteView):
    queryset = RoutingPolicyRule.objects.all()
    default_return_url = 'plugins:netbox_bgp:routingpolicyrule_list'

@register_model_view(RoutingPolicyRule, "bulk_delete", path="delete", detail=False)
class RoutingPolicyRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = RoutingPolicyRule.objects.all()
    table = tables.RoutingPolicyRuleTable

@register_model_view(RoutingPolicyRule)
class RoutingPolicyRuleView(generic.ObjectView):
    queryset = RoutingPolicyRule.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            panels.RoutingPolicyRulePanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
            PluginContentPanel('left_page'),
        ],
        right_panels=[
            # A TemplatePanel rather than a JSONPanel, which renders JSON only: the format
            # switch below lets these be read as YAML too, and match_statements and
            # set_statements are properties whose contents are easier to scan that way.
            TemplatePanel(
                'netbox_bgp/inc/routingpolicyrule_statements.html',
                title=_('Statements'),
            ),
            PluginContentPanel('right_page'),
        ],
        bottom_panels=[
            PluginContentPanel('full_width_page'),
        ],
    )

    def get_extra_context(self, request, instance):
        # Remember the chosen format on the user's config, as the template did before, so
        # the choice persists across rules.
        if request.GET.get('format') in ['json', 'yaml']:
            format = request.GET.get('format')
            if request.user.is_authenticated:
                request.user.config.set('data_format', format, commit=True)
        elif request.user.is_authenticated:
            format = request.user.config.get('data_format', 'json')
        else:
            format = 'json'

        return {
            'format': format,
        }


@register_model_view(RoutingPolicyRule, "bulk_import", path="import", detail=False)
class RoutingPolicyRuleImportView(generic.BulkImportView):
    queryset = RoutingPolicyRule.objects.all()
    model_form = forms.RoutingPolicyRuleImportForm

# Peer Group

@register_model_view(BGPPeerGroup, "list", path="", detail=False)
class BGPPeerGroupListView(generic.ObjectListView):
    queryset = BGPPeerGroup.objects.all()
    filterset = filtersets.BGPPeerGroupFilterSet
    filterset_form = forms.BGPPeerGroupFilterForm
    table = tables.BGPPeerGroupTable

@register_model_view(BGPPeerGroup, "add", detail=False)
@register_model_view(BGPPeerGroup, "edit")
class BGPPeerGroupEditView(generic.ObjectEditView):
    queryset = BGPPeerGroup.objects.all()
    form = forms.BGPPeerGroupForm

@register_model_view(BGPPeerGroup, "bulk_delete", path="delete", detail=False)
class BGPPeerGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = BGPPeerGroup.objects.all()
    table = tables.BGPPeerGroupTable

@register_model_view(BGPPeerGroup)
class BGPPeerGroupView(generic.ObjectView):
    queryset = BGPPeerGroup.objects.all()
    template_name = 'generic/object.html'
    layout = layout.Layout(
        layout.Row(
            layout.Column(
                panels.BGPPeerGroupPanel(),
                CustomFieldsPanel(),
                TagsPanel(),
                JSONPanel('extra_attributes', title=_('Extra Attributes')),
                CommentsPanel(),
                PluginContentPanel('left_page'),
            ),
            layout.Column(
                ContextTablePanel('import_policies_table', title=_('Import Policies')),
                ContextTablePanel('export_policies_table', title=_('Export Policies')),
                PluginContentPanel('right_page'),
            ),
        ),
        layout.Row(
            layout.Column(
                ContextTablePanel(
                    'related_session_table', title=_('Related BGP Sessions')
                ),
                PluginContentPanel('full_width_page'),
            ),
        ),
    )

    def get_extra_context(self, request, instance):
        import_policies_table = tables.RoutingPolicyTable(
            instance.import_policies.all(),
            orderable=False
        )
        import_policies_table.configure(request)
        export_policies_table = tables.RoutingPolicyTable(
            instance.export_policies.all(),
            orderable=False
        )
        export_policies_table.configure(request)

        sess = BGPSession.objects.filter(peer_group=instance)
        sess = sess.distinct()
        sess_table = tables.BGPSessionTable(sess)
        sess_table.configure(request)
        return {
            'import_policies_table': import_policies_table,
            'export_policies_table': export_policies_table,
            'related_session_table': sess_table
        }

@register_model_view(BGPPeerGroup, "delete")
class BGPPeerGroupDeleteView(generic.ObjectDeleteView):
    queryset = BGPPeerGroup.objects.all()
    default_return_url = 'plugins:netbox_bgp:bgppeergroup_list'

@register_model_view(BGPPeerGroup, "bulk_import", path="import", detail=False)
class BGPPeerGroupBulkImportView(generic.BulkImportView):
    queryset = BGPPeerGroup.objects.all()
    model_form = forms.BGPPeerGroupImportForm

@register_model_view(BGPPeerGroup, "bulk_edit", path="edit", detail=False)
class BGPPeerGroupBulkEditView(generic.BulkEditView):
    queryset = BGPPeerGroup.objects.all()
    filterset = filtersets.BGPPeerGroupFilterSet
    table = tables.BGPPeerGroupTable
    form = forms.BGPPeerGroupBulkEditForm


# Prefix List

@register_model_view(PrefixList, "list", path="", detail=False)
class PrefixListListView(generic.ObjectListView):
    queryset = PrefixList.objects.all()
    filterset = filtersets.PrefixListFilterSet
    filterset_form = forms.PrefixListFilterForm
    table = tables.PrefixListTable

@register_model_view(PrefixList, "add", detail=False)
@register_model_view(PrefixList, "edit")
class PrefixListEditView(generic.ObjectEditView):
    queryset = PrefixList.objects.all()
    form = forms.PrefixListForm

@register_model_view(PrefixList, "bulk_delete", path="delete", detail=False)
class PrefixListBulkDeleteView(generic.BulkDeleteView):
    queryset = PrefixList.objects.all()
    table = tables.PrefixListTable

@register_model_view(PrefixList, "bulk_edit", path="edit", detail=False)
class PrefixListBulkEditView(generic.BulkEditView):
    queryset = PrefixList.objects.all()
    filterset = filtersets.PrefixListFilterSet
    table = tables.PrefixListTable
    form = forms.PrefixListBulkEditForm

@register_model_view(PrefixList)
class PrefixListView(generic.ObjectView):
    queryset = PrefixList.objects.all()
    template_name = 'generic/object.html'
    layout = layout.Layout(
        layout.Row(
            layout.Column(
                panels.PrefixListPanel(),
                CustomFieldsPanel(),
                TagsPanel(),
                CommentsPanel(),
                PluginContentPanel('left_page'),
            ),
            layout.Column(
                ContextTablePanel(
                    'rprules_table', title=_('Related Routing Policy Rules')
                ),
                ContextTablePanel('sess_table', title=_('Related BGP Sessions')),
                PluginContentPanel('right_page'),
            ),
        ),
        layout.Row(
            layout.Column(
                ContextTablePanel(
                    'rules_table',
                    title=_('Rules'),
                    actions=[
                        panel_actions.AddObject(
                            'netbox_bgp.prefixlistrule',
                            url_params={'prefix_list': lambda ctx: ctx['object'].pk},
                            label=_('Rule'),
                        ),
                    ],
                ),
                PluginContentPanel('full_width_page'),
            ),
        ),
    )

    def get_extra_context(self, request, instance):
        rprules_table = tables.RoutingPolicyRuleTable(instance.plrules.all())
        rprules_table.configure(request)
        rules_table = tables.PrefixListRuleTable(instance.prefrules.all())
        rules_table.configure(request)

        sess = instance.session_prefix_in.all() | instance.session_prefix_out.all()
        sess_table = tables.BGPSessionTable(sess)
        sess_table.configure(request)
        return {
            'rules_table': rules_table,
            'rprules_table': rprules_table,
            'sess_table': sess_table,
        }

@register_model_view(PrefixList, "delete")
class PrefixListDeleteView(generic.ObjectDeleteView):
    queryset = PrefixList.objects.all()
    default_return_url = 'plugins:netbox_bgp:prefixlist_list'

@register_model_view(PrefixList, "bulk_import", path="import", detail=False)
class PrefixListBulkImportView(generic.BulkImportView):
    queryset = PrefixList.objects.all()
    model_form = forms.PrefixListImportForm


# Prefix List Rule

@register_model_view(PrefixListRule, "list", path="", detail=False)
class PrefixListRuleListView(generic.ObjectListView):
    queryset = PrefixListRule.objects.all()
    filterset = filtersets.PrefixListRuleFilterSet
    table = tables.PrefixListRuleTable
    actions = (AddObject, BulkImport, BulkExport, BulkDelete)

@register_model_view(PrefixListRule, "add", detail=False)
@register_model_view(PrefixListRule, "edit")
class PrefixListRuleEditView(generic.ObjectEditView):
    queryset = PrefixListRule.objects.all()
    form = forms.PrefixListRuleForm

@register_model_view(PrefixListRule, "bulk_delete", path="delete", detail=False)
class PrefixListRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = PrefixListRule.objects.all()
    table = tables.PrefixListRuleTable

@register_model_view(PrefixListRule, "delete")
class PrefixListRuleDeleteView(generic.ObjectDeleteView):
    queryset = PrefixListRule.objects.all()
    default_return_url = 'plugins:netbox_bgp:prefixlistrule_list'

@register_model_view(PrefixListRule)
class PrefixListRuleView(generic.ObjectView):
    queryset = PrefixListRule.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            panels.PrefixListRulePanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
            PluginContentPanel('left_page'),
        ],
        right_panels=[
            PluginContentPanel('right_page'),
        ],
        bottom_panels=[
            PluginContentPanel('full_width_page'),
        ],
    )


@register_model_view(PrefixListRule, "bulk_import", path="import", detail=False)
class PrefixListRuleViewImportView(generic.BulkImportView):
    queryset = PrefixListRule.objects.all()
    model_form = forms.PrefixListRuleImportForm


# Viewtab for Virtual Machine

@register_model_view(VirtualMachine, name='bgpsessions', path='bgpsessions')
class VMBGPSessionView(generic.ObjectChildrenView):
    queryset = VirtualMachine.objects.all().prefetch_related('bgpsession_set')
    child_model = BGPSession
    table = tables.BGPSessionTable
    template_name = "generic/object_children.html"
    tab = ViewTab(
        label='BGP Sessions',
        badge=lambda obj:  obj.bgpsession_set.count(),
        hide_if_empty = True
    )

    def get_children(self, request, parent):
        return parent.bgpsession_set.all()

# AS Path List

@register_model_view(ASPathList, "list", path="", detail=False)
class ASPathListListView(generic.ObjectListView):
    queryset = ASPathList.objects.all()
    filterset = filtersets.ASPathListFilterSet
    filterset_form = forms.ASPathListFilterForm
    table = tables.ASPathListTable

@register_model_view(ASPathList, "add", detail=False)
@register_model_view(ASPathList, "edit")
class ASPathListEditView(generic.ObjectEditView):
    queryset = ASPathList.objects.all()
    form = forms.ASPathListForm

@register_model_view(ASPathList, "bulk_delete", path="delete", detail=False)
class ASPathListBulkDeleteView(generic.BulkDeleteView):
    queryset = ASPathList.objects.all()
    table = tables.ASPathListTable

@register_model_view(ASPathList, "bulk_edit", path="edit", detail=False)
class ASPathListBulkEditView(generic.BulkEditView):
    queryset = ASPathList.objects.all()
    filterset = filtersets.ASPathListFilterSet
    table = tables.ASPathListTable
    form = forms.ASPathListBulkEditForm

@register_model_view(ASPathList)
class ASPathListView(generic.ObjectView):
    queryset = ASPathList.objects.all()
    template_name = 'generic/object.html'
    layout = layout.Layout(
        layout.Row(
            layout.Column(
                panels.ASPathListPanel(),
                CustomFieldsPanel(),
                TagsPanel(),
                CommentsPanel(),
                PluginContentPanel('left_page'),
            ),
            layout.Column(
                ContextTablePanel(
                    'rprules_table', title=_('Related Routing Policy Rules')
                ),
                PluginContentPanel('right_page'),
            ),
        ),
        layout.Row(
            layout.Column(
                ContextTablePanel(
                    'rules_table',
                    title=_('Rules'),
                    actions=[
                        panel_actions.AddObject(
                            'netbox_bgp.aspathlistrule',
                            url_params={'aspath_list': lambda ctx: ctx['object'].pk},
                            label=_('Rule'),
                        ),
                    ],
                ),
                PluginContentPanel('full_width_page'),
            ),
        ),
    )

    def get_extra_context(self, request, instance):
        rprules_table = tables.RoutingPolicyRuleTable(instance.aspathrules.all())
        rprules_table.configure(request)
        rules_table = tables.ASPathListRuleTable(instance.aspathlistrules.all())
        rules_table.configure(request)
        return {
            'rules_table': rules_table,
            'rprules_table': rprules_table
        }

@register_model_view(ASPathList, "delete")
class ASPathListDeleteView(generic.ObjectDeleteView):
    queryset = ASPathList.objects.all()
    default_return_url = 'plugins:netbox_bgp:aspathlist_list'

@register_model_view(ASPathList, "bulk_import", path="import", detail=False)
class ASPathListBulkImportView(generic.BulkImportView):
    queryset = ASPathList.objects.all()
    model_form = forms.ASPathListImportForm

# AS Path List Rule

@register_model_view(ASPathListRule, "list", path="", detail=False)
class ASPathListRuleListView(generic.ObjectListView):
    queryset = ASPathListRule.objects.all()
    filterset = filtersets.ASPathListRuleFilterSet
    # filterset_form = ASPathListRuleFilterForm
    table = tables.ASPathListRuleTable
    actions = (AddObject, BulkImport, BulkExport, BulkDelete)


@register_model_view(ASPathListRule, "add", detail=False)
@register_model_view(ASPathListRule, "edit")
class ASPathListRuleEditView(generic.ObjectEditView):
    queryset = ASPathListRule.objects.all()
    form = forms.ASPathListRuleForm


@register_model_view(ASPathListRule, "bulk_delete", path="delete", detail=False)
class ASPathListRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = ASPathListRule.objects.all()
    table = tables.ASPathListRuleTable


@register_model_view(ASPathListRule, "delete")
class ASPathListRuleDeleteView(generic.ObjectDeleteView):
    queryset = ASPathListRule.objects.all()
    default_return_url = 'plugins:netbox_bgp:aspathlistrule_list'


@register_model_view(ASPathListRule, "bulk_import", path="import", detail=False)
class ASPathListRuleBulkImportView(generic.BulkImportView):
    queryset = ASPathListRule.objects.all()
    model_form = forms.ASPathListRuleImportForm


@register_model_view(ASPathListRule)
class ASPathListRuleView(generic.ObjectView):
    queryset = ASPathListRule.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            panels.ASPathListRulePanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
            PluginContentPanel('left_page'),
        ],
        right_panels=[
            PluginContentPanel('right_page'),
        ],
        bottom_panels=[
            PluginContentPanel('full_width_page'),
        ],
    )
