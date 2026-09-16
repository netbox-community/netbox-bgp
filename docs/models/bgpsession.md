# BGP Sessions

A BGP session records a single peering relationship: the local end (a Device or Virtual
Machine, with an address and an AS) and the remote end (an address or a prefix, with an
AS). It is the plugin's central object; most other models exist to be referenced by one.

## Fields

### Name

An optional free-text name, up to 256 characters. When it is left blank the session is
labelled `<remote peer>:<remote AS>` instead — for example `192.0.2.1/32:65001`. Nothing in
the plugin assumes a session has a name.

### Device and Virtual Machine

The local end of the session. Both fields are optional individually, and in practice a
session should have exactly one of them.

!!! warning
    This is not currently enforced. The validation that would require one or the other is
    present in the model but disabled, so a session with neither can be created through the
    REST API. The uniqueness rules below are scoped per-device and per-VM, which means
    unattached sessions are not deduplicated either.

### Local Address

**Required.** The `ipam.IPAddress` the local end peers from. Protected: the address cannot
be deleted while a session references it.

### Remote Address

The `ipam.IPAddress` of the remote neighbour, for a conventional session with a single
peer. Mutually exclusive with Remote Prefix — set exactly one.

On the **Add Session** form this field accepts a free-text CIDR by default and creates the
`IPAddress` if it does not exist. That behaviour is governed by
[`remote_address_strict`](../configuration.md#remote_address_strict) and applies to the add
form only; the edit form, the REST API, and bulk import all require an existing object.

### Remote Prefix

An `ipam.Prefix` standing in for the remote end, documenting dynamic peering — where the
device accepts sessions from any address within a subnet (`bgp listen range` on
Cisco/Arista, `allow` on Juniper). Mutually exclusive with Remote Address.

!!! note
    A Remote Prefix is never auto-created. The `ipam.Prefix` must already exist, regardless
    of the `remote_address_strict` setting.

Sessions with a Remote Prefix appear on the [BGP Sessions tab of that Prefix](../integrations.md#the-prefix-tab).

### Local AS and Remote AS

**Required.** The `ipam.ASN` at each end. Both are protected against deletion while
referenced.

### Remote AS Macro

An optional free-text field, up to 255 characters, recording an AS macro or IRR as-set name
for the remote side — for example `AS-EXAMPLE`. The plugin stores it as a label only: it
performs no validation, expansion, or IRR lookup. It is available for filtering and global
search.

### Status

The operational state of the session. One of:

| Value     | Label   |
|-----------|---------|
| `offline` | Offline |
| `active`  | Active  |
| `planned` | Planned |
| `failed`  | Failed  |

Defaults to Active.

### Peer Group

An optional [Peer Group](./bgppeergroup.md). Referencing a group does **not** cause the
group's settings to be applied to this session; see
[Defaults are not inherited](./bgppeergroup.md#defaults-are-not-inherited).

### Import and Export Policies

Many-to-many references to [Routing Policies](./routingpolicy.md). These are always the
session's own policies — the UI and REST API never merge in the peer group's.

### Prefix List In and Out

Optional [Prefix Lists](./prefixlist.md) filtering routes in each direction.

### Max Prefixes

An optional positive integer recording the session's maximum-prefix limit. Must be at least
1 if set. The plugin does not enforce it against anything; it is documentation.

### Site and Tenant

Optional `dcim.Site` and `tenancy.Tenant` assignments. Both drive a
[BGP Sessions tab](../integrations.md) on the respective object.

### Extra Attributes

A free-form JSON object for configuration data the plugin does not model explicitly.
NetBox stores and returns it as-is; no schema is enforced. Useful for feeding attributes
through to configuration templating or external automation. Defaults to an empty object.

## Uniqueness

Two sets of rules apply, depending on which kind of remote end the session has:

* **Address-based sessions** must be unique on
  `(device, local_address, local_as, remote_address, remote_as)`, and on the equivalent
  tuple with `virtualmachine` in place of `device`.

* **Prefix-based sessions** must be unique on
  `(device, local_address, local_as, remote_prefix, remote_as)`, and the VM equivalent.
  These are conditional constraints, applied only where the relevant fields are non-null.

The split exists because `remote_prefix` is nullable, and a NULL member would make
PostgreSQL treat every row as distinct — which would silently disable the address-based
rules if the two were combined into one constraint.
