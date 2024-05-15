from django import forms
from utilities.forms.rendering import FieldSet
from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
    ValidationError,
)
from django.utils.translation import gettext as _

from tenancy.models import Tenant
from dcim.models import Device, Site
from ipam.models import IPAddress, Prefix, ASN
from ipam.formfields import IPNetworkFormField
from utilities.forms.fields import (
    DynamicModelChoiceField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    CommentField,
)
from utilities.forms.widgets import APISelect, APISelectMultiple
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
)

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
)

from .choices import (
    SessionStatusChoices,
    CommunityStatusChoices,
    IPAddressFamilyChoices,
)


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

    tag = TagFilterField(model)


class CommunityListForm(NetBoxModelForm):

    comments = CommentField()

    class Meta:
        model = CommunityList
        fields = ["name", "description", "tags", "comments"]


class CommunityListBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)

    model = CommunityList
    nullable_fields = [
        "description",
    ]


class CommunityListImportForm(NetBoxModelImportForm):

    class Meta:
        model = CommunityList
        fields = ("name", "description", "tags")


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
    name = forms.CharField(max_length=64, required=True)
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(), required=False, query_params={"site_id": "$site"}
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
    site = DynamicModelChoiceField(
        label=_("Site"), queryset=Site.objects.all(), required=False
    )
    status = forms.ChoiceField(
        label=_("Status"),
        required=False,
        choices=SessionStatusChoices,
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
    ]


class RoutingPolicyFilterForm(NetBoxModelFilterSetForm):
    model = RoutingPolicy
    q = forms.CharField(required=False, label="Search")

    tag = TagFilterField(model)


class RoutingPolicyForm(NetBoxModelForm):

    comments = CommentField()

    class Meta:
        model = RoutingPolicy
        fields = ["name", "description", "tags", "comments"]


class RoutingPolicyImportForm(NetBoxModelImportForm):

    class Meta:
        model = RoutingPolicy
        fields = ("name", "description", "tags")


class RoutingPolicyBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)

    model = RoutingPolicy
    nullable_fields = [
        "description",
    ]


class BGPPeerGroupFilterForm(NetBoxModelFilterSetForm):
    model = BGPPeerGroup
    q = forms.CharField(required=False, label="Search")

    tag = TagFilterField(model)


class BGPPeerGroupForm(NetBoxModelForm):
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


class BGPPeerGroupImportForm(NetBoxModelImportForm):

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
        fields = ("name", "description", "import_policies", "export_policies", "tags")


class BGPPeerGroupBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)

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
    nullable_fields = [
        "description", "import_policies", "export_policies"
    ]


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
    match_ip_address = forms.MultipleChoiceField(
        choices=[], required=False, label="Match IPv4 address Prefix lists"
    )

    match_ipv6_address = forms.MultipleChoiceField(
        choices=[], required=False, label="Match IPv6 address Prefix lists"
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
        if instance:
            _prefix_v4 = PrefixList.objects.filter(family="ipv4")
            _prefix_v6 = PrefixList.objects.filter(family="ipv6")
            prefix_v4 = list(set([(prefix.id, prefix.name) for prefix in _prefix_v4]))
            prefix_v6 = list(set([(prefix.id, prefix.name) for prefix in _prefix_v6]))
            self.fields["match_ip_address"].choices = prefix_v4
            self.fields["match_ipv6_address"].choices = prefix_v6

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
            "match_custom",
            "set_actions",
            "description",
            "tags",
            "comments",
        ]


class PrefixListFilterForm(NetBoxModelFilterSetForm):
    model = PrefixList
    q = forms.CharField(required=False, label="Search")

    tag = TagFilterField(model)


class PrefixListForm(NetBoxModelForm):

    comments = CommentField()

    class Meta:
        model = PrefixList
        fields = ["name", "description", "family", "tags", "comments"]


class PrefixListImportForm(NetBoxModelImportForm):
    family = CSVChoiceField(
        choices=IPAddressFamilyChoices, required=True, help_text=_("Family address")
    )

    class Meta:
        model = PrefixList
        fields = ("name", "description", "family", "tags")


class PrefixListBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)

    family = forms.ChoiceField(
        label=_("Family"),
        required=False,
        choices=IPAddressFamilyChoices,
    )

    model = PrefixList
    nullable_fields = [
        "description",
    ]


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
