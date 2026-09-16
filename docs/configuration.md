# Configuration Parameters

This page documents the configuration parameters specific to the NetBox BGP plugin. They
are set under the `netbox_bgp` key of NetBox's `PLUGINS_CONFIG` dictionary, for example:

```python
PLUGINS_CONFIG = {
    'netbox_bgp': {
        'device_ext_page': 'tab',
        'top_level_menu': True,
    },
}
```

Every parameter is optional; the plugin runs with sensible defaults if `PLUGINS_CONFIG`
does not mention it at all.

---

## `device_ext_page`

Default: `'right'`

Controls where a device's BGP sessions appear on the device detail page. One of:

| Value          | Placement                                                        |
|----------------|------------------------------------------------------------------|
| `left`         | In the left column of the device detail page                     |
| `right`        | In the right column of the device detail page                    |
| `full_width`   | Full width, at the bottom of the device detail page              |
| `tab`          | In a dedicated **BGP Sessions** tab                              |
| `''` (empty)   | Disabled — device BGP sessions are not displayed                 |

```python
PLUGINS_CONFIG = {
    'netbox_bgp': {
        'device_ext_page': 'tab',
    }
}
```

!!! warning
    This parameter is read once, when the plugin is loaded. Changing it requires a restart
    of both NetBox and its worker (`systemctl restart netbox netbox-rq`); it does not take
    effect on the next request.

This setting governs the Device page only. The equivalent tabs on Virtual Machines,
Interfaces, IP Addresses, ASNs, Prefixes, Sites, and Tenants are always enabled — see
[Integrations](./integrations.md).

---

## `top_level_menu`

Default: `False`

When `True`, the plugin's objects are grouped under their own top-level **BGP** section in
the NetBox navigation menu. When `False`, they are added to NetBox's existing menu
structure instead.

```python
PLUGINS_CONFIG = {
    'netbox_bgp': {
        'top_level_menu': True,
    }
}
```

---

## `remote_address_strict`

Default: `False`

Controls how the **Add Session** form handles the Remote Address field.

When `False` (the default), the field accepts a free-text CIDR. If no matching
`ipam.IPAddress` exists, one is created when the session is saved.

When `True`, the field becomes a selector limited to existing `IPAddress` objects, matching
the behaviour of the edit form. An unknown address is rejected rather than created.

```python
PLUGINS_CONFIG = {
    'netbox_bgp': {
        'remote_address_strict': True,
    }
}
```

!!! tip
    Enabling this is recommended in multi-VRF environments. A free-text CIDR is matched by
    address alone, so it resolves to the first match when the same address exists in
    several VRFs, and any address it creates is created without a VRF.

!!! note
    This setting applies to Remote Address only. A Remote Prefix must always reference an
    existing `ipam.Prefix` and is never auto-created, regardless of this setting.
