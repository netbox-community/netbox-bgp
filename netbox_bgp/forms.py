from django import forms
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from extras.models import Tag
from tenancy.models import Tenant
from dcim.models import Device, Site
from ipam.models import IPAddress
from ipam.formfields import IPNetworkFormField
from utilities.forms import (
    BootstrapMixin, DynamicModelChoiceField, BulkEditForm,
    DynamicModelMultipleChoiceField, StaticSelect2,
    APISelect, APISelectMultiple, StaticSelect2Multiple, TagFilterField
)

from .models import ASN, ASNStatusChoices, Community, BGPSession, SessionStatusChoices


class ASNFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(
        required=False,
        label='Search'
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    status = forms.MultipleChoiceField(
        choices=ASNStatusChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )

    tag = TagFilterField(ASN)

    class Meta:
        model = ASN
        fields = ['q', 'status', 'tenant']


class ASNForm(BootstrapMixin, forms.ModelForm):
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )

    class Meta:
        model = ASN
        fields = [
            'number', 'description', 'status', 'site', 'tenant', 'tags',
        ]


class ASNBulkEditForm(BootstrapMixin, BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    status = forms.ChoiceField(
        required=False,
        choices=ASNStatusChoices,
        widget=StaticSelect2()
    )

    class Meta:
        nullable_fields = [
            'tenant', 'description',
        ]


class CommunityForm(BootstrapMixin, forms.ModelForm):
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )

    class Meta:
        model = Community
        fields = [
            'value', 'description', 'status', 'tenant', 'tags',
        ]


class CommunityFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(
        required=False,
        label='Search'
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    status = forms.MultipleChoiceField(
        choices=ASNStatusChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )

    tag = TagFilterField(Community)

    class Meta:
        model = Community
        fields = ['q', 'status', 'tenant']


class CommunityBulkEditForm(BootstrapMixin, BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Community.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    status = forms.ChoiceField(
        required=False,
        choices=ASNStatusChoices,
        widget=StaticSelect2()
    )

    class Meta:
        nullable_fields = [
            'tenant', 'description',
        ]


class BGPSessionForm(BootstrapMixin, forms.ModelForm):
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site'
        }
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    local_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        null_option=None,
        query_params={
            'site_id': '$site'
        },
        display_field='number',
        widget=APISelect(
            api_url='/api/plugins/bgp/asn/',
        )

    )
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        query_params={
            'site_id': '$site'
        },
        display_field='number',
        widget=APISelect(
            api_url='/api/plugins/bgp/asn/',
        )

    )
    local_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        display_field='address',
        query_params={
            'device_id': '$device'
        }
    )

    class Meta:
        model = BGPSession
        fields = [
            'site', 'device',
            'local_as', 'remote_as', 'local_address', 'remote_address',
            'description', 'status', 'tenant', 'tags',
        ]


class BGPSessionAddForm(BGPSessionForm):
    remote_address = IPNetworkFormField()

    def clean_remote_address(self):
        try:
            ip = IPAddress.objects.get(address=str(self.cleaned_data['remote_address']))
        except MultipleObjectsReturned:
            ip = IPAddress.objects.filter(address=str(self.cleaned_data['remote_address'])).first()
        except ObjectDoesNotExist:
            ip = IPAddress.objects.create(address=str(self.cleaned_data['remote_address']))
        self.cleaned_data['remote_address'] = ip
        return self.cleaned_data['remote_address']


class BGPSessionFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(
        required=False,
        label='Search'
    )
    remote_as = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        display_field='number',
        widget=APISelectMultiple(
            api_url='/api/plugins/bgp/asn/',
        )
    )
    local_as = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        display_field='number',
        widget=APISelectMultiple(
            api_url='/api/plugins/bgp/asn/',
        )
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    status = forms.MultipleChoiceField(
        choices=SessionStatusChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )

    tag = TagFilterField(BGPSession)

    class Meta:
        model = BGPSession
        fields = ['q', 'status', 'tenant', 'remote_as', 'local_as']
