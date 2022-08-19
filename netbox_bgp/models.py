from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.core.exceptions import FieldError, ValidationError
from django.conf import settings

from taggit.managers import TaggableManager

from netbox.models import NetBoxModel
from netbox.models.features import ChangeLoggingMixin
from ipam.fields import IPNetworkField
from ipam.models import Prefix

from .choices import IPAddressFamilyChoices, ASNStatusChoices, SessionStatusChoices, ActionChoices


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


class PrefixList(NetBoxModel):
    """
    """
    name = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    family = models.CharField(
        max_length=10,
        choices=IPAddressFamilyChoices
    )

    class Meta:
        verbose_name_plural = 'Prefix Lists'
        unique_together = ['name', 'description', 'family']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:prefixlist', args=[self.pk])


class PrefixListRule(NetBoxModel):
    """
    """
    prefix_list = models.ForeignKey(
        to=PrefixList,
        on_delete=models.CASCADE,
        related_name='prefrules'
    )
    index = models.PositiveIntegerField()
    action = models.CharField(
        max_length=30,
        choices=ActionChoices
    )
    prefix = models.ForeignKey(
        to='ipam.Prefix',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.CASCADE,
    )
    prefix_custom = IPNetworkField(
        blank=True,
        null=True,
    )
    ge = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(128)]
    )
    le = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(128)]
    )

    class Meta:
        ordering = ('prefix_list', 'index')
        unique_together = ('prefix_list', 'index')

    @property
    def network(self):
        return self.prefix_custom or self.prefix

    def __str__(self):
        return f'{self.prefix_list}: Rule {self.index}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:prefixlistrule', args=[self.pk])

    def get_action_color(self):
        return ActionChoices.colors.get(self.action)

    def clean(self):
        super().clean()
        # make sure that only one field is setted
        if self.prefix and self.prefix_custom:
            raise ValidationError(
                    {'prefix': 'Cannot set both fields'}
                )
        # at least one fields must be setted
        if self.prefix is None and self.prefix_custom is None:
            raise ValidationError(
                    {'prefix': 'Cannot set both fields to Null'}
                )


class RoutingPolicyRule(NetBoxModel):
    routing_policy = models.ForeignKey(
        to=RoutingPolicy,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    index = models.PositiveIntegerField()
    action = models.CharField(
        max_length=30,
        choices=ActionChoices
    )
    description = models.CharField(
        max_length=500,
        blank=True
    )
    continue_entry = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    match_community = models.ManyToManyField(
        to=Community,
        blank=True,
        related_name='+'
    )
    match_ip_address = models.ManyToManyField(
        to=PrefixList,
        blank=True,
        related_name='plrules',
    )
    match_ipv6_address = models.ManyToManyField(
        to=PrefixList,
        blank=True,
        related_name='plrules6',
    )
    match_custom = models.JSONField(
        blank=True,
        null=True,
    )
    set_actions = models.JSONField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('routing_policy', 'index')
        unique_together = ('routing_policy', 'index')

    def __str__(self):
        return f'{self.routing_policy}: Rule {self.index}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_bgp:routingpolicyrule', args=[self.pk])

    def get_action_color(self):
        return ActionChoices.colors.get(self.action)

    def get_match_custom(self):
        # some kind of ckeck?
        result = {}
        if self.match_custom:
            result = self.match_custom
        return result

    @property
    def match_statements(self):
        result = {}
        # add communities
        result.update(
            {'community': list(self.match_community.all().values_list('value', flat=True))}
        )
        result.update(
            {'ip address': [str(prefix_list) for prefix_list in self.match_ip_address.all().values_list('name', flat=True)]}
        )
        result.update(
            {'ipv6 address': [str(prefix_list) for prefix_list in self.match_ipv6_address.all().values_list('name', flat=True)]}
        )

        custom_match = self.get_match_custom()
        # update community from custom
        result['community'].extend(custom_match.get('community', []))
        result['ip address'].extend(custom_match.get('ip address', []))
        result['ipv6 address'].extend(custom_match.get('ipv6 address', []))
        # remove empty matches
        result = {k: v for k, v in result.items() if v}
        return result

    @property
    def set_statements(self):
        if self.set_actions:
            return self.set_actions
        return {}
