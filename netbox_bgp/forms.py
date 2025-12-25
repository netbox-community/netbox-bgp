from django import forms
from utilities.forms.rendering import FieldSet
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
    ValidationError,
)
from django.utils.translation import gettext as _

from tenancy.models import Tenant
from dcim.models import Device, Location, Rack, Region, Site, SiteGroup
from ipam.models import IPAddress, Prefix, ASN, VRF
from ipam.formfields import IPNetworkFormField
from ipam.constants import VLANGROUP_SCOPE_TYPES
from utilities.forms.fields import (
    DynamicModelChoiceField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    CommentField,
    ContentTypeChoiceField,
    CSVContentTypeField,
)
from utilities.forms import add_blank_choice
from utilities.forms.widgets import APISelect, APISelectMultiple, HTMXSelect
from utilities.forms.utils import get_field_value
from utilities.templatetags.builtins.filters import bettertitle
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
)
from .choices import SessionStatusChoices, ActionChoices

from .models import (
    Community,
    BGPSession,
    RoutingPolicy,
    BGPPeerGroup,
    RoutingPolicyRule,
    PrefixList,
    PrefixListRule,
    CommunityList,
    CommunityListRule,
    ASPathList,
    ASPathListRule,
    Redistributing,
)

from .choices import (
    SessionStatusChoices,
    CommunityStatusChoices,
    IPAddressFamilyChoices,
    RedistributeSourceChoices,
)

from virtualization.models import Cluster, ClusterGroup, VirtualMachine

class ASPathListFilterForm(NetBoxModelFilterSetForm):
    model = ASPathList
    q = forms.CharField(required=False, label="Search")

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )
    site_group = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_("Site group")
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site")
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location")
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_("Rack")
    )
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_("Cluster")
    )
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_("Cluster group")
    )
    tag = TagFilterField(model)

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("region", "site_group", "site", "location", "rack", name=_("Location")),
        FieldSet("cluster_group", "cluster", name=_("Cluster")),
    )

class ASPathListRuleFilterForm(NetBoxModelFilterSetForm):
    model = ASPathListRule
    q = forms.CharField(required=False, label="Search")
    aspath_list = DynamicModelChoiceField(queryset=ASPathList.objects.all(), required=False)
    tag = TagFilterField(model)

    
class ASPathListForm(NetBoxModelForm):
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    comments = CommentField()

    fieldsets = (
        FieldSet("name", "description", "tags"),
        FieldSet("scope_type", "scope", name=_("Scope")),
    )

    nullable_fields = [
        "scope"
    ]

    class Meta:
        model = ASPathList
        fields = ["name", "description", "tags", "comments"]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})

        if instance and getattr(instance, "scope", None):
            scope = ContentType.objects.get_for_model(instance.scope)
            initial["scope_type"] = scope.pk
            initial["scope"] = instance.scope.pk
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, 'scope_type'):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all().order_by("name")
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                self.fields["scope"].queryset = Site.objects.none()
                self.fields["scope"].disabled = True

    def clean(self):
        super().clean()

        # Assign the selected scope (if any)
        self.instance.scope = self.cleaned_data.get("scope")



class ASPathListBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(method="post", attrs={"hx-select": "#form_fields"}),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )

    model = ASPathList
    fieldsets = (
        FieldSet("description", "tag"),
        FieldSet("scope_type", "scope",  name=_("Scope")),
    )
    nullable_fields = [
        "description",
        "scope",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, "scope_type"):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all()
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

class ASPathListImportForm(NetBoxModelImportForm):
    scope_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        required=False,
        label=_('Scope type (app & model)')
    )

    class Meta:
        model = ASPathList
        fields = ["name", "description", "scope_type", "scope_id", "tags"]
        labels = {
            "scope_id": "Scope ID",
        }


class ASPathListRuleImportForm(NetBoxModelImportForm):
    aspath_list = CSVModelChoiceField(
        label=_('AS Path List'),
        queryset=ASPathList.objects.all(),
        to_field_name='name'
    )
    action = CSVChoiceField(
        label=_('Action'),
        choices=ActionChoices
    )

    class Meta:
        model = ASPathListRule
        fields = ["aspath_list", "index", "action", "pattern", "description", "tags", "comments"]   


class ASPathListRuleForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = ASPathListRule
        fields = ["aspath_list", "index", "action", "pattern", "description", "tags", "comments"]


class CommunityForm(NetBoxModelForm):
    status = forms.ChoiceField(
        required=False,
        choices=CommunityStatusChoices,
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    comments = CommentField()

    class Meta:
        model = Community
        fields = ["value", "description", "status", "tenant", "tags", "comments"]


class CommunityFilterForm(NetBoxModelFilterSetForm):
    q = forms.CharField(required=False, label="Search")
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    status = forms.MultipleChoiceField(
        choices=CommunityStatusChoices,
        required=False,
    )
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)

    tag = TagFilterField(Community)

    model = Community


class CommunityBulkEditForm(NetBoxModelBulkEditForm):
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    description = forms.CharField(max_length=200, required=False)
    status = forms.ChoiceField(
        required=False,
        choices=CommunityStatusChoices,
    )

    model = Community
    nullable_fields = [
        "tenant",
        "description",
    ]


class CommunityImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned tenant"),
    )

    status = CSVChoiceField(
        choices=CommunityStatusChoices, help_text=_("Operational status")
    )

    class Meta:
        model = Community
        fields = ("value", "description", "tags")


class CommunityListFilterForm(NetBoxModelFilterSetForm):
    model = CommunityList
    q = forms.CharField(required=False, label="Search")

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )
    site_group = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_("Site group")
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site")
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location")
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_("Rack")
    )
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_("Cluster")
    )
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_("Cluster group")
    )
    tag = TagFilterField(model)

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("region", "site_group", "site", "location", "rack", name=_("Location")),
        FieldSet("cluster_group", "cluster", name=_("Cluster")),
    )

class CommunityListForm(NetBoxModelForm):
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    comments = CommentField()

    fieldsets = (
        FieldSet("name", "description", "tags"),
        FieldSet("scope_type", "scope", name=_("Scope")),
    )

    nullable_fields = [
        "scope"
    ]

    class Meta:
        model = CommunityList
        fields = ["name", "description", "tags", "comments"]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})

        if instance and getattr(instance, "scope", None):
            scope = ContentType.objects.get_for_model(instance.scope)
            initial["scope_type"] = scope.pk
            initial["scope"] = instance.scope.pk
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, 'scope_type'):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all().order_by("name")
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                self.fields["scope"].queryset = Site.objects.none()
                self.fields["scope"].disabled = True

    def clean(self):
        super().clean()

        # Assign the selected scope (if any)
        self.instance.scope = self.cleaned_data.get("scope")

class CommunityListBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(method="post", attrs={"hx-select": "#form_fields"}),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )

    model = CommunityList
    fieldsets = (
        FieldSet("description", "tag"),
        FieldSet("scope_type", "scope",  name=_("Scope")),
    )
    nullable_fields = [
        "description",
        "scope",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, "scope_type"):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all()
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

class CommunityListImportForm(NetBoxModelImportForm):
    scope_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        required=False,
        label=_('Scope type (app & model)')
    )

    class Meta:
        model = CommunityList
        fields = ("name", "description", "scope_type", "scope_id", "tags")
        labels = {
            "scope_id": "Scope ID",
        }

class CommunityListRuleForm(NetBoxModelForm):
    community = DynamicModelChoiceField(
        queryset=Community.objects.all(),
        required=False,
        help_text="Community",
    )

    comments = CommentField()

    class Meta:
        model = CommunityListRule
        fields = ["community_list", "action", "community", "tags", "comments"]


class BGPSessionForm(NetBoxModelForm):
    name = forms.CharField(max_length=64, required=False)
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(), required=False, query_params={"site_id": "$site"}
    )
    virtualmachine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(), required=False, query_params={"site_id": "$site"}
    )

    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    local_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        query_params={"site_id": "$site"},
        label=_("Local AS"),
    )
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(), label=_("Remote AS")
    )
    local_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(), query_params={"device_id": "$device"}
    )
    remote_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
    )
    peer_group = DynamicModelChoiceField(
        queryset=BGPPeerGroup.objects.all(),
        required=False,
        widget=APISelect(
            api_url="/api/plugins/bgp/peer-group/",
        ),
    )
    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    prefix_list_in = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        widget=APISelect(
            api_url="/api/plugins/bgp/prefix-list/",
        ),
    )
    prefix_list_out = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        widget=APISelect(
            api_url="/api/plugins/bgp/prefix-list/",
        ),
    )
    comments = CommentField()


    fieldsets = (
        FieldSet(
            "name",
            "description",
            "site",
            "device",
            "virtualmachine",
            "status",
            "peer_group",
            "tenant",
            "tags",
            name="Session",
        ),
        FieldSet("remote_as", "remote_address", name="Remote"),
        FieldSet("local_as", "local_address", name="Local"),
        FieldSet("import_policies", "export_policies", name="Policies"),
        FieldSet("prefix_list_in", "prefix_list_out", name="Prefixes"),
    )

    class Meta:
        model = BGPSession
        fields = [
            "name",
            "site",
            "device",
            "virtualmachine",
            "local_as",
            "remote_as",
            "local_address",
            "remote_address",
            "description",
            "status",
            "peer_group",
            "tenant",
            "tags",
            "import_policies",
            "export_policies",
            "prefix_list_in",
            "prefix_list_out",
            "comments",
        ]

        widgets = {
            "status": forms.Select(),
        }


class BGPSessionAddForm(BGPSessionForm):
    remote_address = IPNetworkFormField()

    def clean_remote_address(self):
        try:
            ip = IPAddress.objects.get(address=str(self.cleaned_data["remote_address"]))
        except MultipleObjectsReturned:
            ip = IPAddress.objects.filter(
                address=str(self.cleaned_data["remote_address"])
            ).first()
        except ObjectDoesNotExist:
            ip = IPAddress.objects.create(
                address=str(self.cleaned_data["remote_address"])
            )
        self.cleaned_data["remote_address"] = ip
        return self.cleaned_data["remote_address"]


class BGPSessionImportForm(NetBoxModelImportForm):
    site = CSVModelChoiceField(
        label=_("Site"),
        required=False,
        queryset=Site.objects.all(),
        to_field_name="name",
        help_text=_("Assigned site"),
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned tenant"),
    )
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        help_text=_("Assigned device"),
        required=False,
    )
    virtualmachine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        to_field_name="name",
        help_text=_("Assigned virtual machine"),
        required=False,
    )
    status = CSVChoiceField(
        choices=SessionStatusChoices, required=False, help_text=_("Operational status")
    )
    local_address = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        to_field_name="address",
        help_text=_("Local IP Address"),
    )
    remote_address = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        to_field_name="address",
        help_text=_("Remote IP Address"),
    )
    local_as = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        to_field_name="asn",
        help_text=_("Local ASN"),
    )
    remote_as = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        to_field_name="asn",
        help_text=_("Remote ASN"),
    )
    peer_group = CSVModelChoiceField(
        queryset=BGPPeerGroup.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Peer Group"),
    )
    import_policies = CSVModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        to_field_name="name",
        required=False,
        help_text=_("Import policies name"),
    )
    export_policies = CSVModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        to_field_name="name",
        required=False,
        help_text=_("Export policies name"),
    )
    prefix_list_in = CSVModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Prefix list In"),
    )
    prefix_list_out = CSVModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Prefix List Out"),
    )

    class Meta:
        model = BGPSession
        fields = [
            "name",
            "device",
            "virtualmachine",
            "site",
            "description",
            "tenant",
            "status",
            "peer_group",
            "import_policies",
            "export_policies",
            "local_address",
            "remote_address",
            "local_as",
            "remote_as",
            "tags",
            "prefix_list_in",
            "prefix_list_out",
        ]


class BGPSessionFilterForm(NetBoxModelFilterSetForm):
    model = BGPSession
    q = forms.CharField(required=False, label="Search")
    remote_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(), required=False, label=_("Remote AS")
    )
    local_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(), required=False, label=_("Local AS")
    )
    by_local_address = forms.CharField(required=False, label="Local Address")
    by_remote_address = forms.CharField(required=False, label="Remote Address")
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label=_("Device")
    )
    virtualmachine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(), required=False, label=_("VirtualMachine")
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(), required=False, label=_("Site")
    )
    status = forms.MultipleChoiceField(
        choices=SessionStatusChoices,
        required=False,
    )
    peer_group = DynamicModelMultipleChoiceField(
        queryset=BGPPeerGroup.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/peer-group/"),
    )
    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    prefix_list_in = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/prefix-list/"),
    )
    prefix_list_out = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/prefix-list/"),
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    tag = TagFilterField(model)


class BGPSessionBulkEditForm(NetBoxModelBulkEditForm):
    device = DynamicModelChoiceField(
        label=_("Device"),
        queryset=Device.objects.all(),
        required=False,
    )
    virtualmachine = DynamicModelChoiceField(
        label=_("Virtual Machine"),
        queryset=VirtualMachine.objects.all(),
        required=False,
    )
    site = DynamicModelChoiceField(
        label=_("Site"), queryset=Site.objects.all(), required=False
    )
    status = forms.ChoiceField(
        label=_('Status'),
        choices=add_blank_choice(SessionStatusChoices),
        required=False
    )
    description = forms.CharField(
        label=_("Description"), max_length=200, required=False
    )
    tenant = DynamicModelChoiceField(
        label=_("Tenant"), queryset=Tenant.objects.all(), required=False
    )
    local_as = DynamicModelChoiceField(queryset=ASN.objects.all(), required=False)
    remote_as = DynamicModelChoiceField(queryset=ASN.objects.all(), required=False)
    peer_group = DynamicModelChoiceField(
        queryset=BGPPeerGroup.objects.all(),
        required=False,
        widget=APISelect(
            api_url="/api/plugins/bgp/peer-group/",
        ),
    )
    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )

    model = BGPSession

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "site",
            "device",
            "virtualmachine",
            "status",
            "peer_group",
            "tenant",
            "tags",
            name="Session",
        ),
        FieldSet("remote_as", "remote_address", name="Remote"),
        FieldSet("local_as", "local_address", name="Local"),
        FieldSet("import_policies", "export_policies", name="Policies"),
        FieldSet("prefix_list_in", "prefix_list_out", name="Prefixes"),
    )

    nullable_fields = [
        "tenant",
        "description",
        "peer_group",
        "import_policies",
        "export_policies",
        "prefix_list_in",
        "prefix_list_out",
        "site",
    ]


class RoutingPolicyFilterForm(NetBoxModelFilterSetForm):
    model = RoutingPolicy
    q = forms.CharField(required=False, label="Search")

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )
    site_group = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_("Site group")
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site")
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location")
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_("Rack")
    )
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_("Cluster")
    )
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_("Cluster group")
    )
    tag = TagFilterField(model)

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("region", "site_group", "site", "location", "rack", name=_("Location")),
        FieldSet("cluster_group", "cluster", name=_("Cluster")),
    )

class RoutingPolicyForm(NetBoxModelForm):
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    comments = CommentField()

    fieldsets = (
        FieldSet("name", "description", "weight", "tags"),
        FieldSet("scope_type", "scope", name=_("Scope")),
    )

    nullable_fields = [
        "scope"
    ]

    class Meta:
        model = RoutingPolicy
        fields = ["name", "description", "weight", "tags", "comments"]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})

        if instance and getattr(instance, "scope", None):
            scope = ContentType.objects.get_for_model(instance.scope)
            initial["scope_type"] = scope.pk
            initial["scope"] = instance.scope.pk
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, 'scope_type'):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all().order_by("name")
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                self.fields["scope"].queryset = Site.objects.none()
                self.fields["scope"].disabled = True

    def clean(self):
        super().clean()

        # Assign the selected scope (if any)
        self.instance.scope = self.cleaned_data.get("scope")

class RoutingPolicyImportForm(NetBoxModelImportForm):
    scope_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        required=False,
        label=_('Scope type (app & model)')
    )

    class Meta:
        model = RoutingPolicy
        fields = ("name", "description", "scope_type", "scope_id", "weight", "tags")
        labels = {
            "scope_id": "Scope ID",
        }

class RoutingPolicyBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(method="post", attrs={"hx-select": "#form_fields"}),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )

    model = RoutingPolicy
    fieldsets = (
        FieldSet("description", "tag"),
        FieldSet("scope_type", "scope",  name=_("Scope")),
    )
    nullable_fields = [
        "description",
        "scope",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, "scope_type"):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all()
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

class BGPPeerGroupFilterForm(NetBoxModelFilterSetForm):
    model = BGPPeerGroup
    q = forms.CharField(required=False, label="Search")

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )
    site_group = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_("Site group")
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site")
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location")
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_("Rack")
    )
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_("Cluster")
    )
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_("Cluster group")
    )
    tag = TagFilterField(model)

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("region", "site_group", "site", "location", "rack", name=_("Location")),
        FieldSet("cluster_group", "cluster", name=_("Cluster")),
    )

class BGPPeerGroupForm(NetBoxModelForm):
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    comments = CommentField()

    fieldsets = (
        FieldSet("name", "description", "import_policies", "export_policies", "tags"),
        FieldSet("scope_type", "scope", name=_("Scope")),
    )

    nullable_fields = [
        "scope"
    ]

    class Meta:
        model = BGPPeerGroup
        fields = [
            "name",
            "description",
            "import_policies",
            "export_policies",
            "tags",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})

        if instance and getattr(instance, "scope", None):
            scope = ContentType.objects.get_for_model(instance.scope)
            initial["scope_type"] = scope.pk
            initial["scope"] = instance.scope.pk
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, 'scope_type'):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all().order_by("name")
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                self.fields["scope"].queryset = Site.objects.none()
                self.fields["scope"].disabled = True

    def clean(self):
        super().clean()

        # Assign the selected scope (if any)
        self.instance.scope = self.cleaned_data.get("scope")

class BGPPeerGroupImportForm(NetBoxModelImportForm):
    scope_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        required=False,
        label=_('Scope type (app & model)')
    )
    import_policies = CSVModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        to_field_name="name",
        required=False,
        help_text=_("Import policies name"),
    )
    export_policies = CSVModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        to_field_name="name",
        required=False,
        help_text=_("Export policies name"),
    )

    class Meta:
        model = BGPPeerGroup
        fields = ("name", "description", "scope_type", "scope_id", "import_policies", "export_policies", "tags")
        labels = {
            "scope_id": "Scope ID",
        }

class BGPPeerGroupBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(method="post", attrs={"hx-select": "#form_fields"}),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )

    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )

    model = BGPPeerGroup
    fieldsets = (
        FieldSet("description", "import_policies", "export_policies", "tag"),
        FieldSet("scope_type", "scope",  name=_("Scope")),
    )
    nullable_fields = [
        "description", "scope", "import_policies", "export_policies"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, "scope_type"):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all()
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

class RoutingPolicyRuleForm(NetBoxModelForm):
    continue_entry = forms.IntegerField(
        required=False,
        label="Continue",
        help_text="Null for disable, 0 to next entry, or any sequence number",
    )
    match_community = DynamicModelMultipleChoiceField(
        queryset=Community.objects.all(),
        required=False,
    )
    match_community_list = DynamicModelMultipleChoiceField(
        queryset=CommunityList.objects.all(),
        required=False,
    )
    
    match_ip_address = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        query_params={
            'family': 'ipv4'
        }
    )

    match_ipv6_address = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        query_params={
            'family': 'ipv6'
        }
    )

    match_aspath_list = DynamicModelMultipleChoiceField(
        queryset=ASPathList.objects.all(),
        required=False,
    )   

    match_custom = forms.JSONField(
        label="Custom Match",
        help_text='Any custom match statements, e.g., {"ip nexthop": "1.1.1.1"}',
        required=False,
    )
    set_actions = forms.JSONField(
        label="Set statements",
        help_text='Set statements, e.g., {"as-path prepend": [12345,12345]}',
        required=False,
    )
    comments = CommentField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance", {})

    class Meta:
        model = RoutingPolicyRule
        fields = [
            "routing_policy",
            "index",
            "action",
            "continue_entry",
            "match_community",
            "match_community_list",
            "match_ip_address",
            "match_ipv6_address",
            "match_aspath_list",
            "match_custom",
            "set_actions",
            "description",
            "tags",
            "comments",
        ]

class RoutingPolicyRuleImportForm(NetBoxModelImportForm):
    routing_policy = CSVModelChoiceField(
        label=_('Routing policy'),
        queryset=RoutingPolicy.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Routing policy')
    )
    action = CSVChoiceField(
        label=_('Action'),
        choices=ActionChoices
    )
    match_community = CSVModelMultipleChoiceField(
        label=_('Match Community'),
        queryset=Community.objects.all(),
        required=False,
        to_field_name='value'
    )
    match_community_list = CSVModelMultipleChoiceField(
        label=_('Match Community List'),
        queryset=CommunityList.objects.all(),
        required=False,
        to_field_name='name',
    )
    match_aspath_list = CSVModelMultipleChoiceField(
        label=_('Match AS Path List'),
        queryset=ASPathList.objects.all(),
        required=False,
        to_field_name='name'
    )
    match_ip_address = CSVModelMultipleChoiceField(
        label=_('Match IPv4 by Prefix List'),
        queryset=PrefixList.objects.all(),
        required=False,
        to_field_name='name',
    )

    match_ipv6_address = CSVModelMultipleChoiceField(
        label=_('Match IPv6 by Prefix List'),
        queryset=PrefixList.objects.all(),
        required=False,
        to_field_name='name',
    )

    class Meta:
        model = RoutingPolicyRule
        fields = (
            "routing_policy",
            "index",
            "action",
            "continue_entry",
            "match_community",
            "match_community_list",
            "match_aspath_list",
            "match_ip_address",
            "match_ipv6_address",
            "match_custom",
            "set_actions",
            "description",
            "tags",
            "comments",
        )



class PrefixListFilterForm(NetBoxModelFilterSetForm):
    model = PrefixList
    q = forms.CharField(required=False, label="Search")

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )
    site_group = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_("Site group")
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site")
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location")
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_("Rack")
    )
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_("Cluster")
    )
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_("Cluster group")
    )
    tag = TagFilterField(model)

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("region", "site_group", "site", "location", "rack", name=_("Location")),
        FieldSet("cluster_group", "cluster", name=_("Cluster")),
    )

class PrefixListForm(NetBoxModelForm):
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    comments = CommentField()

    fieldsets = (
        FieldSet("name", "description", "family", "tags"),
        FieldSet("scope_type", "scope", name=_("Scope")),
    )

    nullable_fields = [
        "scope"
    ]

    class Meta:
        model = PrefixList
        fields = ["name", "description", "family", "tags", "comments"]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})

        if instance and getattr(instance, "scope", None):
            scope = ContentType.objects.get_for_model(instance.scope)
            initial["scope_type"] = scope.pk
            initial["scope"] = instance.scope.pk
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, 'scope_type'):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all().order_by("name")
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                self.fields["scope"].queryset = Site.objects.none()
                self.fields["scope"].disabled = True

    def clean(self):
        super().clean()

        # Assign the selected scope (if any)
        self.instance.scope = self.cleaned_data.get("scope")

class PrefixListImportForm(NetBoxModelImportForm):
    family = CSVChoiceField(
        choices=IPAddressFamilyChoices, required=True, help_text=_("Family address")
    )
    scope_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        required=False,
        label=_('Scope type (app & model)')
    )

    class Meta:
        model = PrefixList
        fields = ("name", "description", "family", "scope_type", "scope_id", "tags")
        labels = {
            "scope_id": "Scope ID",
        }

class PrefixListBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)

    family = forms.ChoiceField(
        label=_("Family"),
        required=False,
        choices=IPAddressFamilyChoices,
    )

    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(method="post", attrs={"hx-select": "#form_fields"}),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )

    model = PrefixList
    fieldsets = (
        FieldSet("description", "family", "tag"),
        FieldSet("scope_type", "scope",  name=_("Scope")),
    )
    nullable_fields = [
        "description",
        "scope",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, "scope_type"):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all()
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

class PrefixListRuleImportForm(NetBoxModelImportForm):
    prefix_list = CSVModelChoiceField(
        label=_('Prefix List'),
        queryset=PrefixList.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Prefix List')
    )
    prefix = CSVModelChoiceField(
        queryset=Prefix.objects.all(),
        to_field_name='prefix',
        required=False,
        help_text=_('Prefix')
    )

    class Meta:
        model = PrefixListRule
        fields = (
            "prefix_list",
            "index",
            "action",
            "prefix",
            "prefix_custom",
            "ge",
            "le",
            "tags",
            "comments",
        )
        
class PrefixListRuleForm(NetBoxModelForm):
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        help_text="NetBox Prefix Object",
    )
    prefix_custom = IPNetworkFormField(
        required=False,
        label="Prefix",
        help_text="Just IP field for define special prefix like 0.0.0.0/0",
    )
    ge = forms.IntegerField(
        label="Greater than or equal to",
        required=False,
    )
    le = forms.IntegerField(
        label="Less than or equal to",
        required=False,
    )
    comments = CommentField()

    class Meta:
        model = PrefixListRule
        fields = [
            "prefix_list",
            "index",
            "action",
            "prefix",
            "prefix_custom",
            "ge",
            "le",
            "tags",
            "comments",
        ]


class RedistributingForm(NetBoxModelForm):
    name = forms.CharField(max_length=256, required=True)
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    vrf = DynamicModelChoiceField(label="VRF", queryset=VRF.objects.all(), required=False)
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(), required=False, query_params={"site_id": "$site"}
    )
    virtualmachine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(), required=False, query_params={"site_id": "$site"}
    )
    redistribute_source = forms.ChoiceField(
        required=True,
        choices=RedistributeSourceChoices,
    )
    redistribute_policy = DynamicModelChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=True,
        query_params={"site_id": "$site"},
        widget=APISelect(api_url="/api/plugins/bgp/routing-policy/"),
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    comments = CommentField()

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "vrf",
            "device",
            "virtualmachine",
            "redistribute_source",
            "redistribute_policy",
            "tags"
        ),
        FieldSet("scope_type", "scope", name=_("Scope")),
        FieldSet("tenant", name=_("Tenancy")),
    )

    nullable_fields = [
        "tenant",
        "scope",
        "vrf",
    ]

    class Meta:
        model = Redistributing
        fields = [
            "name",
            "description",
            "vrf",
            "device",
            "virtualmachine",
            "redistribute_source",
            "redistribute_policy",
            "tenant",
            "tags",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})

        if instance and getattr(instance, "scope", None):
            scope = ContentType.objects.get_for_model(instance.scope)
            initial["scope_type"] = scope.pk
            initial["scope"] = instance.scope.pk
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, 'scope_type'):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all().order_by("name")
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                self.fields["scope"].queryset = Site.objects.none()
                self.fields["scope"].disabled = True

    def clean(self):
        super().clean()

        # Assign the selected scope (if any)
        self.instance.scope = self.cleaned_data.get("scope")

class RedistributingImportForm(NetBoxModelImportForm):
    scope_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        required=False,
        label=_('Scope type (app & model)')
    )
    vrf = CSVModelChoiceField(
        label=_("VRF"),
        required=False,
        queryset=VRF.objects.all(),
        to_field_name="name",
        help_text=_("Assigned VRF"),
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned tenant"),
    )
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned device"),
    )
    virtualmachine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned virtual machine"),
    )
    redistribute_source = CSVChoiceField(
        choices=RedistributeSourceChoices, required=True, help_text=_("Redistribute source")
    )
    redistribute_policy = CSVModelChoiceField(
        queryset=RoutingPolicy.objects.all(),
        to_field_name="name",
        required=False,
        help_text=_("Routing policy name"),
    )

    class Meta:
        model = Redistributing
        fields = [
            "name",
            "description",
            "scope_type",
            "scope_id",
            "vrf",
            "device",
            "virtualmachine",
            "redistribute_source",
            "redistribute_policy",
            "tenant",
            "tags",
            "comments",
        ]
        labels = {
            "scope_id": "Scope ID",
        }


class RedistributingFilterForm(NetBoxModelFilterSetForm):
    model = Redistributing
    q = forms.CharField(required=False, label="Search")
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(), required=False, label=_("VRF")
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label=_("Device")
    )
    virtualmachine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(), required=False, label=_("VirtualMachine")
    )
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )
    site_group = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_("Site group")
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site")
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location")
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_("Rack")
    )
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_("Cluster")
    )
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_("Cluster group")
    )
    redistribute_source = forms.MultipleChoiceField(
        choices=RedistributeSourceChoices,
        required=False,
    )
    redistribute_policy = DynamicModelChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelect(api_url="/api/plugins/bgp/routing-policy/"),
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    tag = TagFilterField(model)

    fieldsets = (
        FieldSet(
            "q",
            "filter_id",
            "vrf_id",
            "device_id",
            "virtualmachine_id",
            "redistribute_source",
            "redistribute_policy",
            "tag"
        ),
        FieldSet("region", "site_group", "site", "location", "rack", name=_("Location")),
        FieldSet("cluster_group", "cluster", name=_("Cluster")),
        FieldSet("tenant", name=_("Tenancy")),
    )

class RedistributingBulkEditForm(NetBoxModelBulkEditForm):
    device = DynamicModelChoiceField(
        label=_("Device"),
        queryset=Device.objects.all(),
        required=False,
    )
    virtualmachine = DynamicModelChoiceField(
        label=_("Virtual Machine"),
        queryset=VirtualMachine.objects.all(),
        required=False,
    )
    vrf = DynamicModelChoiceField(
        label=_("VRF"), queryset=VRF.objects.all(), required=False
    )
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=VLANGROUP_SCOPE_TYPES),
        widget=HTMXSelect(method="post", attrs={"hx-select": "#form_fields"}),
        required=False,
        label=_("Scope type")
    )
    scope = DynamicModelChoiceField(
        label=_("Scope"),
        queryset=Site.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    redistribute_source = forms.ChoiceField(
        label=_('Redistribute source'),
        choices=add_blank_choice(RedistributeSourceChoices),
        required=True
    )
    redistribute_policy = DynamicModelChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelect(api_url="/api/plugins/bgp/routing-policy/"),
    )
    description = forms.CharField(
        label=_("Description"), max_length=200, required=False
    )
    tenant = DynamicModelChoiceField(
        label=_("Tenant"), queryset=Tenant.objects.all(), required=False
    )

    model = Redistributing
    fieldsets = (
        FieldSet("description", "vrf", "device", "virtualmachine", "redistribute_source", "redistribute_policy", "tag"),
        FieldSet("scope_type", "scope",  name=_("Scope")),
        FieldSet("tenant", name=_("Tenancy")),
    )
    nullable_fields = [
        "tenant",
        "description",
        "scope",
        "vrf",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, "scope_type"):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields["scope"].queryset = model.objects.all()
                self.fields["scope"].widget.attrs["selector"] = model._meta.label_lower
                self.fields["scope"].disabled = False
                self.fields["scope"].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass