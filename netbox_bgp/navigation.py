from django.conf import settings

from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu


_menu_items = (
    PluginMenuItem(
        link='plugins:netbox_bgp:community_list',
        link_text='Communities',
        permissions=['netbox_bgp.view_community'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:community_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_bgp.add_community'],
            ),
            PluginMenuButton(
                link='plugins:netbox_bgp:community_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_bgp.add_community'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:communitylist_list',
        link_text='Community Lists',
        permissions=['netbox_bgp.view_communitylist'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:communitylist_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_bgp.add_communitylist'],
            ),
            PluginMenuButton(
                link='plugins:netbox_bgp:communitylist_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_bgp.add_communitylist'],
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
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_bgp.add_bgpsession'],
            ),
            PluginMenuButton(
                link='plugins:netbox_bgp:bgpsession_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_bgp.add_bgpsession'],
            )
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_bgp:routingpolicy_list',
        link_text='Routing Policies',
        permissions=['netbox_bgp.view_routingpolicy'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_bgp:routingpolicy_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_bgp.add_routingpolicy'],
            ),
            PluginMenuButton(
                link='plugins:netbox_bgp:routingpolicy_import',
                title='Import',
                icon_class='mdi mdi-upload',
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
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_bgp.add_prefixlist'],
            ),
            PluginMenuButton(
                link='plugins:netbox_bgp:prefixlist_import',
                title='Import',
                icon_class='mdi mdi-upload',
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
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_bgp.add_bgppeergroup'],
            ),
            PluginMenuButton(
                link='plugins:netbox_bgp:bgppeergroup_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_bgp.add_bgppeergroup'],
            ),
        ),
    )
)

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_bgp', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="BGP",
        groups=(("BGP", _menu_items),),
        icon_class="mdi mdi-bootstrap",
    )
else:
    menu_items = _menu_items
