# Permissions

The plugin follows NetBox's standard permission model. There is nothing plugin-specific
to configure: create a [Permission](https://docs.netbox.dev/en/stable/administration/permissions/)
under **Admin → Permissions**, assign it to a user or a group, and pick the models and
actions it grants.

## Model Permissions

Every plugin model has the four standard NetBox actions: `view`, `add`, `change`, and
`delete`. The permission name follows the pattern `netbox_bgp.<action>_<model>`.

| Model              | Permission prefix                | Notes                                   |
|---------------------|-----------------------------------|------------------------------------------|
| BGP Session          | `netbox_bgp.*_bgpsession`         |                                            |
| Peer Group           | `netbox_bgp.*_bgppeergroup`       |                                            |
| Community            | `netbox_bgp.*_community`          |                                            |
| Community List       | `netbox_bgp.*_communitylist`      |                                            |
| Community List Rule  | `netbox_bgp.*_communitylistrule`  | No dedicated bulk import view             |
| Routing Policy       | `netbox_bgp.*_routingpolicy`      |                                            |
| Routing Policy Rule  | `netbox_bgp.*_routingpolicyrule`  |                                            |
| Prefix List          | `netbox_bgp.*_prefixlist`         |                                            |
| Prefix List Rule     | `netbox_bgp.*_prefixlistrule`     |                                            |
| AS Path List         | `netbox_bgp.*_aspathlist`         |                                            |
| AS Path List Rule    | `netbox_bgp.*_aspathlistrule`     |                                            |

`view_<model>` controls read access, including the REST API and GraphQL. `add_<model>`,
`change_<model>`, and `delete_<model>` control write access the same way they do for any
NetBox model.

## Object-Level Constraints

A NetBox Permission can also carry **constraints** — a filter, expressed as JSON, that
limits the permission to a subset of objects rather than every object of that type. For
example, this constraint limits a `view_bgpsession` permission to sessions belonging to
one tenant:

```json
{"tenant__name": "Customer A"}
```

See NetBox's
[object-based permissions](https://docs.netbox.dev/en/stable/administration/permissions/#object-based-permissions)
documentation for the constraint syntax. This plugin's views honor these constraints
everywhere `view_bgpsession` (or any other plugin model permission) applies — including
the two areas below.

!!! note "Since 0.20.1"
    Object-level constraints on plugin models were not honored in the two areas below
    before 0.20.1. A user could see data past their constraint, or past a missing
    `view_bgpsession` permission entirely, through a tab or a related-object table. Both
    gaps are closed as of 0.20.1.

## BGP Sessions Tabs on Core Objects

The [BGP Sessions tabs](./integrations.md) added to Device, Virtual Machine, Interface,
IP Address, ASN, Prefix, Site, and Tenant each require `netbox_bgp.view_bgpsession`.

A tab's own `view_<parent model>` permission — for example `dcim.view_device` — only
governs whether the user may open the parent object at all. It does not grant BGP
Session visibility. Without `view_bgpsession`, the tab link does not appear in
navigation, and the tab's own page returns no sessions if opened directly.

With `view_bgpsession`, the tab lists only the sessions that permission allows — every
session, if the permission carries no constraint, or only the matching subset, if it
does.

## Related-Object Tables on Detail Pages

Several of the plugin's own detail pages include a table of related objects, built from
a different model than the page itself:

| Detail page     | Related table                       | Required permission                                    |
|------------------|--------------------------------------|----------------------------------------------------------|
| BGP Session      | Import/Export Policies               | `netbox_bgp.view_routingpolicy`                          |
| Routing Policy   | Related Sessions                     | `netbox_bgp.view_bgpsession`                             |
| Routing Policy   | Rules                                | `netbox_bgp.view_routingpolicyrule`                      |
| Peer Group       | Import/Export Policies               | `netbox_bgp.view_routingpolicy`                          |
| Peer Group       | Related Sessions                     | `netbox_bgp.view_bgpsession`                             |
| Prefix List      | Rules                                | `netbox_bgp.view_prefixlistrule`                         |
| Prefix List      | Matching Routing Policy Rules        | `netbox_bgp.view_routingpolicyrule`                      |
| Prefix List      | Related Sessions                     | `netbox_bgp.view_bgpsession`                             |
| Community List   | Rules                                | `netbox_bgp.view_communitylistrule`                      |
| Community List   | Matching Routing Policy Rules        | `netbox_bgp.view_routingpolicyrule`                      |
| AS Path List     | Rules                                | `netbox_bgp.view_aspathlistrule`                         |
| AS Path List     | Matching Routing Policy Rules        | `netbox_bgp.view_routingpolicyrule`                      |

A user needs `view_<page's own model>` to open the page at all. Each related table then
needs its own permission, from the table above, before it shows any rows. A user with
neither permission still opens the page; the related tables are just empty.
