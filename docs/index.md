# NetBox BGP

[NetBox](https://github.com/netbox-community/netbox) models the physical and logical
network, but it has no native representation of BGP. This plugin adds one: the sessions a
device or virtual machine runs, the peer groups they belong to, and the policy objects —
communities, community lists, routing policies, prefix lists, and AS path lists — that
those sessions reference.

Everything is documentation of intent. The plugin does not talk to your routers, generate
configuration, or verify that what you have recorded matches the running network. It gives
you a structured, queryable source of truth that your own tooling can render into
configuration or check against.

## Features

* BGP Sessions attached to a Device or a Virtual Machine, with local and remote addressing
  and AS numbers drawn from NetBox's own IPAM objects.

* Dynamic peering support: a session can nominate a Prefix instead of a single remote
  address, documenting a `bgp listen range` (Cisco/Arista) or `allow` (Juniper).

* Peer Groups carrying group-wide defaults — local/remote AS, prefix lists, and import and
  export policies.

* Policy objects: Communities, Community Lists, Routing Policies, Prefix Lists, and AS Path
  Lists, each with ordered rules.

* A free-form `extra_attributes` JSON field on Sessions and Peer Groups for configuration
  data the plugin does not model explicitly.

* **BGP Sessions** tabs on eight core NetBox objects, so sessions are reachable from the
  Device, VM, Interface, IP Address, ASN, Prefix, Site, or Tenant you are already looking
  at. See [Integrations](./integrations.md).

* Full REST API and GraphQL coverage, NetBox global search, change logging, journaling,
  tags, and custom fields on every model.

* Compatible with [netbox-branching](https://github.com/netboxlabs/netbox-branching) with
  no additional configuration. See [Branching](./branching.md).

## Terminology

* A **session** is a single BGP peering relationship, recorded against the Device or
  Virtual Machine at one end of it. The other end is either a **remote address** (one
  neighbour) or a **remote prefix** (any neighbour within a subnet).

* A **peer group** collects settings shared by several sessions. The plugin stores these as
  group-wide defaults; it does not merge them into the sessions that reference the group.
  See [Peer Group](./models/bgppeergroup.md#defaults-are-not-inherited).

* A **list** — community list, prefix list, or AS path list — is a named, ordered container
  of **rules**. Each rule carries an `action` of permit or deny. Deleting a list deletes its
  rules.

* A **routing policy** is a named container of ordered rules, where each rule combines match
  conditions with actions to set. It is the plugin's equivalent of a route-map.

## Installation

### 1. Virtual Environment

Activate the Python virtual environment used by NetBox (typically located at
`/opt/netbox/venv/`):

```
source /opt/netbox/venv/bin/activate
```

!!! note
    You may need to modify the `source` command above if your virtual environment has been
    installed in a different location.

### 2. Python Package

Use `pip` to install the package from [PyPI](https://pypi.org/project/netbox-bgp/):

```
pip install netbox-bgp
```

Check the [compatibility matrix](https://github.com/netbox-community/netbox-bgp/blob/main/COMPATIBILITY.md)
first: the NetBox ⇄ plugin version pairing is strict, and installing a mismatched release
will fail at startup or misbehave.

### 3. Enable Plugin

Add `netbox_bgp` to the `PLUGINS` list in `configuration.py`:

```python
PLUGINS = [
    # ...
    'netbox_bgp',
]
```

!!! note
    If there are no plugins already installed, you might need to create this parameter. If
    so, be sure to define `PLUGINS` as a list _containing_ the plugin name as above, rather
    than just the name.

### 4. Persist the Requirement

Add `netbox-bgp` to `local_requirements.txt` in the NetBox root directory, so that the
plugin is reinstalled when NetBox is upgraded:

```
echo netbox-bgp >> /opt/netbox/local_requirements.txt
```

### 5. Configuration

The plugin runs with no configuration. Optional settings are declared under the
`netbox_bgp` key of `PLUGINS_CONFIG`; see the [Configuration](./configuration.md) page for
the full list.

### 6. Database Migrations

Run the included database migrations:

```
cd /opt/netbox/netbox
./manage.py migrate
```

### 7. Restart NetBox

Restart the NetBox services to load the plugin:

```
sudo systemctl restart netbox netbox-rq
```

See the [NetBox plugin documentation](https://docs.netbox.dev/en/stable/plugins/#installing-plugins)
for general guidance on installing plugins.

## Known Limitations

* **A session's peer group settings are not inherited.** A Peer Group carries its own
  `local_as`, `remote_as`, prefix lists, policies, and `extra_attributes`, but the plugin
  never merges them into the sessions that reference the group. A session's
  `import_policies` in the UI and REST API are always its own, never the union with its
  group's. Your tooling must read the group explicitly to apply the defaults.

* **A session is not required to have a Device or a Virtual Machine.** The validation that
  would enforce this is present but disabled, so a session with neither can be created
  through the API. The uniqueness constraints are scoped per-device and per-VM, so
  unattached sessions are also not deduplicated.

* **`remote_as_macro` is a label only.** The plugin performs no validation, expansion, or
  IRR lookup on it.

* **`extra_attributes` and `set_actions` are unvalidated JSON.** NetBox stores and returns
  them as-is; no schema is enforced. They are a deliberate escape hatch, not a modelled
  field.

## Screenshots

BGP Session
![BGP Session](./img/session.png)

BGP Sessions
![BGP Session Table](./img/sessions.png)

Community
![Community](./img/commun.png)

Peer Group
![Peer Group](./img/peer_group.png)

Routing Policy
![Routing Policy](./img/routepolicy.png)

Prefix List
![Prefix List](./img/preflist.png)
