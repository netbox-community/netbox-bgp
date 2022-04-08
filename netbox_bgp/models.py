from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.conf import settings

from taggit.managers import TaggableManager

from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel
from netbox.models.features import ChangeLoggingMixin


class ASNStatusChoices(ChoiceSet):

    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = (
        (STATUS_ACTIVE, 'Active', 'blue'),
        (STATUS_RESERVED, 'Reserved', 'cyan'),
        (STATUS_DEPRECATED, 'Deprecated', 'red'),
    )


class SessionStatusChoices(ChoiceSet):

    STATUS_OFFLINE = 'offline'
    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_FAILED = 'failed'

    CHOICES = (
        (STATUS_OFFLINE, 'Offline', 'orange'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_FAILED, 'Failed', 'red'),
    )


class ASNGroup(ChangeLoggingMixin, models.Model):
    """
    """
    name = models.CharField(
        max_length=100
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name


class RoutingPolicy(NetBoxModel):
    """
    """
    name = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Routing Policies'
        unique_together = ['name', 'description']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:routingpolicy', args=[self.pk])


class BGPPeerGroup(NetBoxModel):
    """
    """
    name = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    import_policies = models.ManyToManyField(
        RoutingPolicy,
        blank=True,
        related_name='group_import_policies'
    )
    export_policies = models.ManyToManyField(
        RoutingPolicy,
        blank=True,
        related_name='group_export_policies'
    )

    class Meta:
        verbose_name_plural = 'Peer Groups'
        unique_together = ['name', 'description']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:bgppeergroup', args=[self.pk])


class BGPBase(NetBoxModel):
    """
    """
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name="%(class)s_related",
        blank=True,
        null=True
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=50,
        choices=ASNStatusChoices,
        default=ASNStatusChoices.STATUS_ACTIVE
    )
    role = models.ForeignKey(
        to='ipam.Role',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        abstract = True


class ASN(BGPBase):

    number = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4294967295)]
    )

    group = models.ForeignKey(
        ASNGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    tags = TaggableManager(through='extras.TaggedItem', related_name='asn_tags')

    clone_fields = ['description', 'status', 'tenant']

    class Meta:
        verbose_name = 'AS Number'
        verbose_name_plural = 'AS Numbers'
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'tenant'],
                name='uniqie_number_tenant'
            ),
            models.UniqueConstraint(
                fields=['number'],
                condition=models.Q(tenant=None),
                name='uniqie_number'
            ),
        ]
        # unique_together = ['number', 'site', 'tenant']

    def get_status_color(self):
        return ASNStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:asn', args=[self.pk])

    def get_asdot(self):
        if self.number > 65535:
            return '{}.{}'.format(self.number // 65536, self.number % 65536)
        else:
            return str(self.number)

    def __str__(self):
        nb_settings = settings.PLUGINS_CONFIG.get('netbox_bgp', {})
        asdot = nb_settings.get('asdot', False)
        if asdot:
            return self.get_asdot()
        return str(self.number)


class Community(BGPBase):
    """
    """
    value = models.CharField(
        max_length=64,
        validators=[RegexValidator(r'\d+:\d+')]
    )

    class Meta:
        verbose_name_plural = 'Communities'

    def __str__(self):
        return self.value

    def get_status_color(self):
        return ASNStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:community', args=[self.pk])


class BGPSession(NetBoxModel):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.PROTECT,
        null=True,
    )
    local_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name='local_address'
    )
    remote_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name='remote_address'
    )
    local_as = models.ForeignKey(
        ASN,
        on_delete=models.PROTECT,
        related_name='local_as'
    )
    remote_as = models.ForeignKey(
        ASN,
        on_delete=models.PROTECT,
        related_name='remote_as'
    )
    status = models.CharField(
        max_length=50,
        choices=SessionStatusChoices,
        default=SessionStatusChoices.STATUS_ACTIVE
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    peer_group = models.ForeignKey(
        BGPPeerGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    import_policies = models.ManyToManyField(
        RoutingPolicy,
        blank=True,
        related_name='session_import_policies'
    )
    export_policies = models.ManyToManyField(
        RoutingPolicy,
        blank=True,
        related_name='session_export_policies'
    )

    afi_safi = None  # for future use

    class Meta:
        verbose_name_plural = 'BGP Sessions'
        unique_together = ['device', 'local_address', 'local_as', 'remote_address', 'remote_as']

    def __str__(self):
        return f'{self.device}:{self.name}'

    def get_status_color(self):
        return SessionStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:bgpsession', args=[self.pk])
