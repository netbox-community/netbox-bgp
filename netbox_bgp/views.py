from netbox.views import generic

from .filters import ASNFilterSet, CommunityFilterSet, BGPSessionFilterSet
from .models import ASN, Community, BGPSession
from .tables import ASNTable, CommunityTable, BGPSessionTable
from .forms import (
    ASNFilterForm, ASNBulkEditForm, ASNForm, CommunityForm,
    CommunityFilterForm, CommunityBulkEditForm, BGPSessionForm,
    BGPSessionFilterForm, BGPSessionAddForm
)


class ASNListView(generic.ObjectListView):
    queryset = ASN.objects.all()
    filterset = ASNFilterSet
    filterset_form = ASNFilterForm
    table = ASNTable
    action_buttons = ()
    template_name = 'netbox_bgp/asn_list.html'


class ASNView(generic.ObjectView):
    queryset = ASN.objects.all()
    template_name = 'netbox_bgp/asn.html'

    def get_extra_context(self, request, instance):
        sess = BGPSession.objects.filter(remote_as=instance) | BGPSession.objects.filter(local_as=instance)
        sess_table = BGPSessionTable(sess)
        return {
            'related_session_table': sess_table
        }


class ASNEditView(generic.ObjectEditView):
    queryset = ASN.objects.all()
    model_form = ASNForm


class ASNBulkDeleteView(generic.BulkDeleteView):
    queryset = ASN.objects.all()
    table = ASNTable


class ASNBulkEditView(generic.BulkEditView):
    queryset = ASN.objects.all()
    filterset = ASNFilterSet
    table = ASNTable
    form = ASNBulkEditForm


class ASNDeleteView(generic.ObjectDeleteView):
    queryset = ASN.objects.all()


class CommunityListView(generic.ObjectListView):
    queryset = Community.objects.all()
    filterset = CommunityFilterSet
    filterset_form = CommunityFilterForm
    table = CommunityTable
    action_buttons = ()
    template_name = 'netbox_bgp/community_list.html'


class CommunityView(generic.ObjectView):
    queryset = Community.objects.all()
    template_name = 'netbox_bgp/community.html'


class CommunityEditView(generic.ObjectEditView):
    queryset = Community.objects.all()
    model_form = CommunityForm


class CommunityBulkDeleteView(generic.BulkDeleteView):
    queryset = Community.objects.all()
    table = CommunityTable


class CommunityBulkEditView(generic.BulkEditView):
    queryset = Community.objects.all()
    filterset = CommunityFilterSet
    table = CommunityTable
    form = CommunityBulkEditForm


class CommunityDeleteView(generic.ObjectDeleteView):
    queryset = Community.objects.all()


class BGPSessionListView(generic.ObjectListView):
    queryset = BGPSession.objects.all()
    filterset = BGPSessionFilterSet
    filterset_form = BGPSessionFilterForm
    table = BGPSessionTable
    action_buttons = ()
    template_name = 'netbox_bgp/bgpsession_list.html'


class BGPSessionEditView(generic.ObjectEditView):
    queryset = BGPSession.objects.all()
    model_form = BGPSessionForm


class BGPSessionAddView(generic.ObjectEditView):
    queryset = BGPSession.objects.all()
    model_form = BGPSessionAddForm


class BGPSessionBulkDeleteView(generic.BulkDeleteView):
    queryset = BGPSession.objects.all()
    table = BGPSessionTable


class BGPSessionView(generic.ObjectView):
    queryset = BGPSession.objects.all()
    template_name = 'netbox_bgp/bgpsession.html'


class BGPSessionDeleteView(generic.ObjectDeleteView):
    queryset = BGPSession.objects.all()
