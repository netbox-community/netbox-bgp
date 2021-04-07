import django_tables2 as tables
from django.utils.safestring import mark_safe

from utilities.tables import (
    BaseTable, ChoiceFieldColumn, ToggleColumn,
)

from tenancy.tables import COL_TENANT

from .models import ASN, Community, BGPSession

AVAILABLE_LABEL = mark_safe('<span class="label label-success">Available</span>')


class ASNTable(BaseTable):
    pk = ToggleColumn()
    number = tables.LinkColumn()
    status = ChoiceFieldColumn(
        default=AVAILABLE_LABEL
    )
    site = tables.LinkColumn()
    tenant = tables.TemplateColumn(
        template_code=COL_TENANT
    )

    class Meta(BaseTable.Meta):
        model = ASN
        fields = ('pk', 'number', 'description', 'status')


class CommunityTable(BaseTable):
    pk = ToggleColumn()
    value = tables.LinkColumn()
    status = ChoiceFieldColumn(
        default=AVAILABLE_LABEL
    )
    tenant = tables.TemplateColumn(
        template_code=COL_TENANT
    )

    class Meta(BaseTable.Meta):
        model = Community
        fields = ('pk', 'value', 'description', 'status')


class BGPSessionTable(BaseTable):
    pk = ToggleColumn()
    id = tables.LinkColumn()
    device = tables.LinkColumn()
    remote_address = tables.LinkColumn()
    remote_as = tables.LinkColumn()
    local_as = tables.LinkColumn()
    site = tables.LinkColumn()
    status = ChoiceFieldColumn(
        default=AVAILABLE_LABEL
    )
    tenant = tables.TemplateColumn(
        template_code=COL_TENANT
    )

    class Meta(BaseTable.Meta):
        model = BGPSession
        fields = (
            'pk', 'id', 'device', 'remote_as', 'remote_address', 'local_as', 'description', 'site', 'status'
        )
