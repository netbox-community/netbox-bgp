# Branching

This plugin works with [netbox-branching](https://github.com/netboxlabs/netbox-branching)
with no additional configuration. Every BGP model inherits `NetBoxModel`, and therefore
`ChangeLoggingMixin`, so all of them are branch-aware automatically: BGP objects can be
created, modified, and deleted inside a branch, and those changes are merged into main
along with everything else.

Nothing needs to be registered, and no resolver or validator has to be written.

## Do Not Exempt This Plugin

BGP objects hold foreign keys to branch-aware core data — Devices, Virtual Machines, IP
Addresses, Prefixes, ASNs, Sites, and Tenants. netbox-branching requires that any model
referencing branch-aware data is itself branch-aware, so exempting the plugin breaks
referential integrity between a branch and main.

```python
# Unsupported — will corrupt relations between branches and main
PLUGINS_CONFIG = {
    'netbox_branching': {
        'exempt_models': ['netbox_bgp.*'],
    },
}
```

!!! warning
    This applies to individual models too, not just the `netbox_bgp.*` wildcard. Exempting
    `netbox_bgp.bgpsession` alone is equally unsafe, because sessions reference Devices and
    IP Addresses that branches do track.

## Install Before Branching

As with any plugin, install or upgrade `netbox-bgp` *before* creating branches where you
can. Branches provisioned against an older schema do not receive new migrations
automatically: they enter the **Pending Migrations** status and need the **Migrate** action
before they can be activated or merged.

A branch created before the plugin was installed will not know about its models at all,
though this generally will not impede the branch's other work.

## What Is Covered

| Concern | Status |
|---|---|
| All 11 BGP models | Branch-aware automatically via `NetBoxModel` |
| Many-to-many fields (policies, match conditions) | Replicated — auto-created through tables are handled by netbox-branching |
| Multi-table inheritance | Not used. `BGPBase` is abstract, so no model is affected by this limitation |
| Custom `save()` / `delete()` side effects | None; there is nothing for branching to miss |
| `serialize_object()` overrides | None; the default representation is used |

For plugin developers, the corresponding requirement on the contributing side is that any
new *data* migration must declare `fake_on_branch`. See
[CONTRIBUTING.md](https://github.com/netbox-community/netbox-bgp/blob/main/CONTRIBUTING.md#data-migrations-and-branching).
