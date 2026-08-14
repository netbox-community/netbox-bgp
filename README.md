# NetBox BGP Plugin

This [Netbox](http://netboxlabs.com/oss/netbox/) plugin introduces support for BGP related objects documentation.

Models include:

* BGP Communities
* BGP Community Lists (and Community List Rules)
* BGP Sessions
* BGP Peer Groups
* Routing Policies (and Routing Policy Rules)
* Prefix Lists (and Prefix List Rules)
* AS Path Lists (and AS Path List Rules)

## Compatibility

See the [compatibility matrix](COMPATIBILITY.md) for supported NetBox versions.

## Installation

The plugin is available as a Python package in pypi and can be installed with pip

```
pip install netbox-bgp
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_bgp']
```
Restart NetBox and add `netbox-bgp` to your local_requirements.txt

See [NetBox Documentation](https://docs.netbox.dev/en/stable/plugins/#installing-plugins) for details

## Configuration

The following options are available:
* `device_ext_page`: String (default right) Device related BGP sessions display mode. The following values are available:
  - `left`: Display BGP sessions in the left column of the device detail page
  - `right`: Display BGP sessions in the right column of the device detail page
  - `full_width`: Display BGP sessions in full width at the bottom of the device detail page
  - `tab`: Display BGP sessions in a dedicated tab on the device detail page
  - Set empty value to disable device BGP sessions display
* `top_level_menu`: Bool (default False) Enable top level section navigation menu for the plugin.
* `remote_address_strict`: Bool (default False) When enabled, the "Add Session" form requires selecting an existing IPAddress object for Remote Address instead of accepting a free-text CIDR (which would otherwise auto-create a new IPAddress). Recommended for multi-VRF environments to avoid orphaned addresses and ambiguous matches.

`device_ext_page` is read when the plugin is loaded, so changing it requires a NetBox
restart (and a worker restart) rather than taking effect on the next request.

## Integrations with core NetBox objects

In addition to its own list and detail views, the plugin adds a **BGP Sessions** tab to
several core NetBox objects. Each tab lists the sessions related to the object you are
viewing:

| Object | Sessions shown |
|---|---|
| Device | Sessions whose Device is this device |
| Virtual Machine | Sessions whose Virtual Machine is this VM |
| Interface | Sessions whose local or remote address is an IP assigned to this interface |
| IP Address | Sessions whose local **or** remote address is this IP |
| ASN | Sessions whose local **or** remote AS is this ASN |
| Site | Sessions whose Site is this site |
| Tenant | Sessions whose Tenant is this tenant |

All of these are enabled by default except the Device tab, which is controlled by
`device_ext_page`: set it to `tab` for a dedicated tab, or use `left` / `right` /
`full_width` to render the sessions inline on the device page instead.

## Sessions and Peer Groups

Beyond the usual addressing and AS fields, sessions and peer groups carry a few fields
worth calling out:

* `extra_attributes` (Sessions and Peer Groups): A free-form JSON object for
  configuration data the plugin does not model explicitly. NetBox stores and returns it
  as-is; no schema is enforced. Useful for feeding attributes through to configuration
  templating or external automation.
* `remote_as_macro` (Sessions): A free-text field (max 255 characters) recording an AS
  macro / IRR as-set name (e.g. `AS-EXAMPLE`) for the remote side. The plugin stores it
  as a label only — it performs no validation, expansion, or IRR lookup — and it is
  available for filtering and global search.

A Peer Group carries its own `local_as`, `remote_as`, `prefix_list_in`,
`prefix_list_out`, import/export policies, and `extra_attributes`. These describe
group-wide defaults for your own tooling to apply; the plugin does not merge them into
the sessions that reference the group. In particular, a session's `import_policies` and
`export_policies` in both the UI and the REST API are always the session's own policies,
never the union with its peer group's. Read the peer group explicitly if you need the
group-level values.

## REST API

All endpoints are served under `/api/plugins/bgp/`:

| Endpoint | Model |
|---|---|
| `session/` (alias: `bgpsession/`) | BGP Session |
| `peer-group/` (alias: `bgppeergroup/`) | BGP Peer Group |
| `community/` | Community |
| `community-list/` | Community List |
| `community-list-rule/` | Community List Rule |
| `routing-policy/` | Routing Policy |
| `routing-policy-rule/` | Routing Policy Rule |
| `prefix-list/` | Prefix List |
| `prefix-list-rule/` | Prefix List Rule |
| `aspath-list/` | AS Path List |
| `aspath-list-rule/` | AS Path List Rule |

Sessions and peer groups are each registered under two paths. The `session/` and
`peer-group/` spellings are preferred; `bgpsession/` and `bgppeergroup/` are retained for
backwards compatibility and serve the identical viewset, so existing integrations keep
working.

## GraphQL API

The plugin extends NetBox's GraphQL schema with the following query fields. Each model
provides a single-object field and a `_list` field:

| Model | Single object | List |
|---|---|---|
| Community | `netbox_bgp_community` | `netbox_bgp_community_list` |
| Community List | `netbox_bgp_communitylist` | `netbox_bgp_communitylist_list` |
| Community List Rule | `netbox_bgp_communitylist_rule` | `netbox_bgp_communitylist_rule_list` |
| Session | `netbox_bgp_session` | `netbox_bgp_session_list` |
| Peer Group | `netbox_bgp_peer_group` | `netbox_bgp_peer_group_list` |
| Routing Policy | `netbox_bgp_routing_policy` | `netbox_bgp_routing_policy_list` |
| Routing Policy Rule | `netbox_bgp_routing_policy_rule` | `netbox_bgp_routing_policy_rule_list` |
| Prefix List | `netbox_bgp_prefixlist` | `netbox_bgp_prefixlist_list` |
| Prefix List Rule | `netbox_bgp_prefixlist_rule` | `netbox_bgp_prefixlist_rule_list` |
| AS Path List | `netbox_bgp_aspathlist` | `netbox_bgp_aspathlist_list` |
| AS Path List Rule | `netbox_bgp_aspathlist_rule` | `netbox_bgp_aspathlist_rule_list` |

Note the two similar-looking names: `netbox_bgp_community_list` is the list of
**Communities**, whereas the Community List model is queried via
`netbox_bgp_communitylist` / `netbox_bgp_communitylist_list`.

```graphql
query {
  netbox_bgp_session_list {
    id
    name
    status
    remote_address { address }
    remote_as { asn }
  }
}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development environment, test workflow,
and release conventions.

## Screenshots

BGP Session
![BGP Session](docs/img/session.png)

BGP Sessions
![BGP Session Table](docs/img/sessions.png)

Community
![Community](docs/img/commun.png)

Peer Group
![Peer Group](docs/img/peer_group.png)

Routing Policy
![Routing Policy](docs/img/routepolicy.png)

Prefix List
![Prefix List](docs/img/preflist.png)
