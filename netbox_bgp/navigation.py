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
        permissions=['netbox_bgp.view_asn'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:community_add',
                title='Communities',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_asn'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:session_list',
        link_text='Sessions',
        permissions=['netbox_bgp.view_asn'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:session_add',
                title='Sessions',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_bgp.add_asn'],
            ),
        ),
    )    
)
