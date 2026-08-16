"""
Attribute panels for the plugin's object views.

These replace the hand-written attribute tables that each detail template used to carry.
Labels are stated explicitly wherever the wording differs from what would be derived from
the field name, so the headings match what the templates rendered before.
"""

from django.utils.translation import gettext_lazy as _
from netbox.ui import attrs, panels


class CommunityPanel(panels.ObjectAttributesPanel):
    title = _('Community')

    value = attrs.TextAttr('value')
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True)
    status = attrs.ChoiceAttr('status')
    description = attrs.TextAttr('description')


class CommunityListPanel(panels.ObjectAttributesPanel):
    title = _('Community List')

    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')


class CommunityListRulePanel(panels.ObjectAttributesPanel):
    title = _('Community List Rule')

    # The template used `object.communitylist`, which is not an attribute of the model, so
    # this row rendered as an empty link. The field is `community_list`.
    community_list = attrs.RelatedObjectAttr('community_list', linkify=True, label=_('Community List'))
    action = attrs.ChoiceAttr('action')
    community = attrs.RelatedObjectAttr('community', linkify=True)


class BGPSessionPanel(panels.ObjectAttributesPanel):
    title = _('BGP Session')

    name = attrs.TextAttr('name')
    device = attrs.RelatedObjectAttr('device', linkify=True)
    virtualmachine = attrs.RelatedObjectAttr('virtualmachine', linkify=True, label=_('Virtual Machine'))
    # The template linked this to the device rather than the site.
    site = attrs.RelatedObjectAttr('site', linkify=True)
    local_as = attrs.RelatedObjectAttr('local_as', linkify=True, label=_('Local AS'))
    local_address = attrs.RelatedObjectAttr('local_address', linkify=True, label=_('Local IP'))
    remote_as = attrs.RelatedObjectAttr('remote_as', linkify=True, label=_('Remote AS'))
    remote_as_macro = attrs.TextAttr('remote_as_macro', label=_('Remote AS-MACRO'))
    remote_address = attrs.RelatedObjectAttr('remote_address', linkify=True, label=_('Remote IP'))
    remote_prefix = attrs.RelatedObjectAttr('remote_prefix', linkify=True, label=_('Remote Prefix'))
    status = attrs.ChoiceAttr('status')
    max_prefixes = attrs.NumericAttr('max_prefixes', label=_('Maximum Prefixes'))
    prefix_list_in = attrs.RelatedObjectAttr('prefix_list_in', linkify=True, label=_('Prefix List In'))
    prefix_list_out = attrs.RelatedObjectAttr('prefix_list_out', linkify=True, label=_('Prefix List Out'))
    description = attrs.TextAttr('description')
    peer_group = attrs.RelatedObjectAttr('peer_group', linkify=True, label=_('Peer Group'))
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True)


class BGPPeerGroupPanel(panels.ObjectAttributesPanel):
    title = _('Peer Group')

    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')
    local_as = attrs.RelatedObjectAttr('local_as', linkify=True, label=_('Local AS'))
    remote_as = attrs.RelatedObjectAttr('remote_as', linkify=True, label=_('Remote AS'))
    prefix_list_in = attrs.RelatedObjectAttr('prefix_list_in', linkify=True, label=_('Prefix List (in)'))
    prefix_list_out = attrs.RelatedObjectAttr('prefix_list_out', linkify=True, label=_('Prefix List (out)'))


class RoutingPolicyPanel(panels.ObjectAttributesPanel):
    title = _('Routing Policy')

    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')
    weight = attrs.NumericAttr('weight')


class RoutingPolicyRulePanel(panels.ObjectAttributesPanel):
    title = _('Routing Policy Rule')

    routing_policy = attrs.RelatedObjectAttr('routing_policy', linkify=True, label=_('Routing Policy'))
    index = attrs.NumericAttr('index')
    action = attrs.ChoiceAttr('action')
    description = attrs.TextAttr('description')


class PrefixListPanel(panels.ObjectAttributesPanel):
    title = _('Prefix List')

    name = attrs.TextAttr('name')
    # The field carries choices, so this now shows the label rather than the stored value.
    family = attrs.ChoiceAttr('family')
    description = attrs.TextAttr('description')


class PrefixListRulePanel(panels.ObjectAttributesPanel):
    title = _('Prefix List Rule')

    prefix_list = attrs.RelatedObjectAttr('prefix_list', linkify=True, label=_('Prefix List'))
    index = attrs.NumericAttr('index')
    action = attrs.ChoiceAttr('action')
    # `network` returns either the related Prefix or the rule's own prefix_custom value, so
    # it is only sometimes linkable.
    network = attrs.RelatedObjectAttr('network', linkify=True, label=_('Prefix'))
    ge = attrs.NumericAttr('ge', label=_('Greater than or equal to'))
    le = attrs.NumericAttr('le', label=_('Less than or equal to'))


class ASPathListPanel(panels.ObjectAttributesPanel):
    title = _('AS Path List')

    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')


class ASPathListRulePanel(panels.ObjectAttributesPanel):
    title = _('AS Path List Rule')

    aspath_list = attrs.RelatedObjectAttr('aspath_list', linkify=True, label=_('AS Path List'))
    index = attrs.NumericAttr('index')
    action = attrs.ChoiceAttr('action')
    pattern = attrs.TextAttr('pattern')
    description = attrs.TextAttr('description')
