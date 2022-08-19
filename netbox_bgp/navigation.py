from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_bgp:asn_list',
        link_text='AS Numbers',
        permissions=['netbox_bgp.view_asn'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:asn_add',
                title='AS Numbers',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_asn'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:community_list',
        link_text='Communities',
        permissions=['netbox_bgp.view_community'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:community_add',
                title='Communities',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_community'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:bgpsession_list',
        link_text='Sessions',
        permissions=['netbox_bgp.view_bgpsession'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:bgpsession_add',
                title='Sessions',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_bgpsession'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:routingpolicy_list',
        link_text='Routing Policies',
        permissions=['netbox_bgp.view_routingpolicy'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:routingpolicy_add',
                title='Routing Policies',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_routingpolicy'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:prefixlist_list',
        link_text='Prefix Lists',
        permissions=['netbox_bgp.view_prefixlist'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:prefixlist_add',
                title='Prefix Lists',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_prefixlist'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:bgppeergroup_list',
        link_text='Peer Groups',
        permissions=['netbox_bgp.view_bgppeergroup'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:bgppeergroup_add',
                title='Peer Groups',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_bgppeergroup'],
            ),
        ),
    )
)
