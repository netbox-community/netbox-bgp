
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.text import slugify

from netbox.views import generic
from ipam.models import RIR
from ipam.models import ASN as CoreASN

from .models import (
    ASN, Community, BGPSession, RoutingPolicy,
    BGPPeerGroup, RoutingPolicyRule, PrefixList,
    PrefixListRule
)

from . import forms, tables, filters


# ASN


class ASNListView(generic.ObjectListView):
    queryset = ASN.objects.all()
    filterset = filters.ASNFilterSet
    filterset_form = forms.ASNFilterForm
    table = tables.ASNTable
    action_buttons = ('add',)
    template_name = 'netbox_bgp/asn_list.html'


class ASNView(generic.ObjectView):
    queryset = ASN.objects.all()
    template_name = 'netbox_bgp/asn.html'

    def get_extra_context(self, request, instance):
        sess = BGPSession.objects.filter(remote_as=instance) | BGPSession.objects.filter(local_as=instance)
        sess_table = tables.BGPSessionTable(sess)
        return {
            'related_session_table': sess_table
        }


class ASNEditView(generic.ObjectEditView):
    queryset = ASN.objects.all()
    form = forms.ASNForm


class ASNBulkDeleteView(generic.BulkDeleteView):
    queryset = ASN.objects.all()
    table = tables.ASNTable


class ASNBulkEditView(generic.BulkEditView):
    queryset = ASN.objects.all()
    filterset = filters.ASNFilterSet
    table = tables.ASNTable
    form = forms.ASNBulkEditForm


class ASNDeleteView(generic.ObjectDeleteView):
    queryset = ASN.objects.all()


class ASNMigrateView(generic.BulkDeleteView):
    asn_to_rir = {
        (64496, 64511): 'RFC5398',
        (64512, 65534): 'RFC6996',
        (65536, 65551): 'RFC5398',
        (4200000000, 4294967294): 'RFC6996',
    }
    queryset = ASN.objects.all()
    table = tables.ASNTable
    template_name = 'netbox_bgp/asn_migrate.html'

    def post(self, request, **kwargs):
        model = self.queryset.model

        if request.POST.get('_all'):
            qs = model.objects.all()
            if self.filterset is not None:
                qs = self.filterset(request.GET, qs).qs
            pk_list = qs.only('pk').values_list('pk', flat=True)
        else:
            pk_list = [int(pk) for pk in request.POST.getlist('pk')]

        form_cls = self.get_form()

        if '_confirm' in request.POST:
            form = form_cls(request.POST)
            if form.is_valid():

                # Delete objects
                queryset = self.queryset.filter(pk__in=pk_list)
                deleted_count = queryset.count()
                for asn in queryset:
                    rir_name = 'Default'
                    # get rir name
                    for k, v in self.asn_to_rir.items():
                        if asn.number >= k[0] and asn.number <= k[1]:
                            rir_name = v
                            break
                    rir, _ = RIR.objects.get_or_create(name=rir_name, slug=slugify(rir_name))
                    try:
                        new_asn, new_asn_created = CoreASN.objects.get_or_create(
                            asn=asn.number,
                            description=asn.description,
                            tenant=asn.tenant,
                            rir=rir,
                            custom_field_data=asn.custom_field_data
                        )
                        if new_asn_created:
                            # update tags
                            new_asn.tags.set(asn.tags.all())
                            new_asn.save()
                        else:
                            deleted_count -= 1
                    except Exception:
                        deleted_count -= 1

                msg = f"Migrated {deleted_count} {model._meta.verbose_name_plural}"
                messages.success(request, msg)
                return redirect(reverse('ipam:asn_list'))

        else:
            form = form_cls(initial={
                'pk': pk_list,
                'return_url': self.get_return_url(request),
            })

        # Retrieve objects being deleted
        table = self.table(self.queryset.filter(pk__in=pk_list), orderable=False)
        if not table.rows:
            messages.warning(request, "No {} were selected for migration.".format(model._meta.verbose_name_plural))
            return redirect(self.get_return_url(request))

        return render(request, self.template_name, {
            'form': form,
            'obj_type_plural': model._meta.verbose_name_plural,
            'table': table,
            'return_url': self.get_return_url(request),
        })

# Community


class CommunityListView(generic.ObjectListView):
    queryset = Community.objects.all()
    filterset = filters.CommunityFilterSet
    filterset_form = forms.CommunityFilterForm
    table = tables.CommunityTable
    action_buttons = ('add',)


class CommunityView(generic.ObjectView):
    queryset = Community.objects.all()
    template_name = 'netbox_bgp/community.html'


class CommunityEditView(generic.ObjectEditView):
    queryset = Community.objects.all()
    form = forms.CommunityForm


class CommunityBulkDeleteView(generic.BulkDeleteView):
    queryset = Community.objects.all()
    table = tables.CommunityTable


class CommunityBulkEditView(generic.BulkEditView):
    queryset = Community.objects.all()
    filterset = filters.CommunityFilterSet
    table = tables.CommunityTable
    form = forms.CommunityBulkEditForm


class CommunityDeleteView(generic.ObjectDeleteView):
    queryset = Community.objects.all()
    default_return_url = 'plugins:netbox_bgp:community_list'


# Session


class BGPSessionListView(generic.ObjectListView):
    queryset = BGPSession.objects.all()
    filterset = filters.BGPSessionFilterSet
    filterset_form = forms.BGPSessionFilterForm
    table = tables.BGPSessionTable
    action_buttons = ('add',)
    template_name = 'netbox_bgp/bgpsession_list.html'


class BGPSessionEditView(generic.ObjectEditView):
    queryset = BGPSession.objects.all()
    form = forms.BGPSessionForm


class BGPSessionAddView(generic.ObjectEditView):
    queryset = BGPSession.objects.all()
    form = forms.BGPSessionAddForm


class BGPSessionBulkDeleteView(generic.BulkDeleteView):
    queryset = BGPSession.objects.all()
    table = tables.BGPSessionTable


class BGPSessionView(generic.ObjectView):
    queryset = BGPSession.objects.all()
    template_name = 'netbox_bgp/bgpsession.html'

    def get_extra_context(self, request, instance):
        if instance.peer_group:
            import_policies_qs = instance.import_policies.all() | instance.peer_group.import_policies.all()
            export_policies_qs = instance.export_policies.all() | instance.peer_group.export_policies.all()
        else:
            import_policies_qs = instance.import_policies.all()
            export_policies_qs = instance.export_policies.all()

        import_policies_table = tables.RoutingPolicyTable(
            import_policies_qs,
            orderable=False
        )
        export_policies_table = tables.RoutingPolicyTable(
            export_policies_qs,
            orderable=False
        )

        return {
            'import_policies_table': import_policies_table,
            'export_policies_table': export_policies_table
        }


class BGPSessionDeleteView(generic.ObjectDeleteView):
    queryset = BGPSession.objects.all()
    default_return_url = 'plugins:netbox_bgp:bgpsession_list'

# Routing Policy


class RoutingPolicyListView(generic.ObjectListView):
    queryset = RoutingPolicy.objects.all()
    filterset = filters.RoutingPolicyFilterSet
    filterset_form = forms.RoutingPolicyFilterForm
    table = tables.RoutingPolicyTable
    action_buttons = ('add',)


class RoutingPolicyEditView(generic.ObjectEditView):
    queryset = RoutingPolicy.objects.all()
    form = forms.RoutingPolicyForm


class RoutingPolicyBulkDeleteView(generic.BulkDeleteView):
    queryset = RoutingPolicy.objects.all()
    table = tables.RoutingPolicyTable


class RoutingPolicyView(generic.ObjectView):
    queryset = RoutingPolicy.objects.all()
    template_name = 'netbox_bgp/routingpolicy.html'

    def get_extra_context(self, request, instance):
        sess = BGPSession.objects.filter(
            Q(import_policies=instance)
            | Q(export_policies=instance)
            | Q(peer_group__in=instance.group_import_policies.all())
            | Q(peer_group__in=instance.group_export_policies.all())
        )
        sess = sess.distinct()
        sess_table = tables.BGPSessionTable(sess)
        rules = instance.rules.all()
        rules_table = tables.RoutingPolicyRuleTable(rules)
        return {
            'rules_table': rules_table,
            'related_session_table': sess_table
        }


class RoutingPolicyDeleteView(generic.ObjectDeleteView):
    queryset = RoutingPolicy.objects.all()
    default_return_url = 'plugins:netbox_bgp:routingpolicy_list'


# Peer Group


class BGPPeerGroupListView(generic.ObjectListView):
    queryset = BGPPeerGroup.objects.all()
    filterset = filters.BGPPeerGroupFilterSet
    filterset_form = forms.BGPPeerGroupFilterForm
    table = tables.BGPPeerGroupTable
    action_buttons = ('add',)


class BGPPeerGroupEditView(generic.ObjectEditView):
    queryset = BGPPeerGroup.objects.all()
    form = forms.BGPPeerGroupForm


class BGPPeerGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = BGPPeerGroup.objects.all()
    table = tables.BGPPeerGroupTable


class BGPPeerGroupView(generic.ObjectView):
    queryset = BGPPeerGroup.objects.all()
    template_name = 'netbox_bgp/bgppeergroup.html'

    def get_extra_context(self, request, instance):
        import_policies_table = tables.RoutingPolicyTable(
            instance.import_policies.all(),
            orderable=False
        )
        export_policies_table = tables.RoutingPolicyTable(
            instance.export_policies.all(),
            orderable=False
        )

        sess = BGPSession.objects.filter(peer_group=instance)
        sess = sess.distinct()
        sess_table = tables.BGPSessionTable(sess)
        return {
            'import_policies_table': import_policies_table,
            'export_policies_table': export_policies_table,
            'related_session_table': sess_table
        }


class BGPPeerGroupDeleteView(generic.ObjectDeleteView):
    queryset = BGPPeerGroup.objects.all()
    default_return_url = 'plugins:netbox_bgp:bgppeergroup_list'


# Routing Policy Rule


class RoutingPolicyRuleEditView(generic.ObjectEditView):
    queryset = RoutingPolicyRule.objects.all()
    form = forms.RoutingPolicyRuleForm


class RoutingPolicyRuleDeleteView(generic.ObjectDeleteView):
    queryset = RoutingPolicyRule.objects.all()
    default_return_url = 'plugins:netbox_bgp:routingpolicyrule_list'


class RoutingPolicyRuleView(generic.ObjectView):
    queryset = RoutingPolicyRule.objects.all()
    template_name = 'netbox_bgp/routingpolicyrule.html'

    def get_extra_context(self, request, instance):
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


class RoutingPolicyRuleListView(generic.ObjectListView):
    queryset = RoutingPolicyRule.objects.all()
    # filterset = RoutingPolicyRuleFilterSet
    # filterset_form = RoutingPolicyRuleFilterForm
    table = tables.RoutingPolicyRuleTable
    action_buttons = ('add',)


# Prefix List


class PrefixListListView(generic.ObjectListView):
    queryset = PrefixList.objects.all()
    filterset = filters.PrefixListFilterSet
    filterset_form = forms.PrefixListFilterForm
    table = tables.PrefixListTable
    action_buttons = ('add',)


class PrefixListEditView(generic.ObjectEditView):
    queryset = PrefixList.objects.all()
    form = forms.PrefixListForm


class PrefixListBulkDeleteView(generic.BulkDeleteView):
    queryset = PrefixList.objects.all()
    table = tables.PrefixListTable


class PrefixListView(generic.ObjectView):
    queryset = PrefixList.objects.all()
    template_name = 'netbox_bgp/prefixlist.html'

    def get_extra_context(self, request, instance):
        rprules = instance.plrules.all()
        rprules_table = tables.RoutingPolicyRuleTable(rprules)
        rules = instance.prefrules.all()
        rules_table = tables.PrefixListRuleTable(rules)
        return {
            'rules_table': rules_table,
            'rprules_table': rprules_table
        }


class PrefixListDeleteView(generic.ObjectDeleteView):
    queryset = PrefixList.objects.all()
    default_return_url = 'plugins:netbox_bgp:prefixlist_list'


# Prefix List Rule


class PrefixListRuleListView(generic.ObjectListView):
    queryset = PrefixListRule.objects.all()
    # filterset = RoutingPolicyRuleFilterSet
    # filterset_form = RoutingPolicyRuleFilterForm
    table = tables.PrefixListRuleTable
    action_buttons = ('add',)


class PrefixListRuleEditView(generic.ObjectEditView):
    queryset = PrefixListRule.objects.all()
    form = forms.PrefixListRuleForm


class PrefixListRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = PrefixListRule.objects.all()
    table = tables.PrefixListRuleTable


class PrefixListRuleDeleteView(generic.ObjectDeleteView):
    queryset = PrefixListRule.objects.all()
    default_return_url = 'plugins:netbox_bgp:prefixlistrule_list'


class PrefixListRuleView(generic.ObjectView):
    queryset = PrefixListRule.objects.all()
    template_name = 'netbox_bgp/prefixlistrule.html'
