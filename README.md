# NetBox BGP Plugin

This [NetBox](http://netboxlabs.com/oss/netbox/) plugin introduces support for BGP related objects documentation.

Models include:

* BGP Communities
* BGP Community Lists (and Community List Rules)
* BGP Sessions
* BGP Peer Groups
* Routing Policies (and Routing Policy Rules)
* Prefix Lists (and Prefix List Rules)
* AS Path Lists (and AS Path List Rules)

See the [compatibility matrix](COMPATIBILITY.md) for supported NetBox versions, and the
[changelog](CHANGELOG.md) for release notes and upgrade instructions.

> [!TIP]
> This plugin is compatible with [netbox-branching](https://github.com/netboxlabs/netbox-branching) out of the box. See [Branching](./docs/branching.md) for the one configuration pitfall to avoid.

## Installation

Brief installation instructions are provided below. For a complete installation guide, please refer to the included [documentation](./docs/index.md).

1. Install the plugin from [PyPI](https://pypi.org/project/netbox-bgp/):

```
$ pip install netbox-bgp
```

2. Add `netbox_bgp` to `PLUGINS` in `configuration.py`:

```python
PLUGINS = [
    # ...
    'netbox_bgp',
]
```

3. Add `netbox-bgp` to `local_requirements.txt` so it survives future upgrades.

4. Run NetBox migrations:

```
$ ./manage.py migrate
```

5. Restart NetBox.

## Documentation

| Page | Contents |
|---|---|
| [Introduction](./docs/index.md) | Features, full installation guide, screenshots |
| [Configuration](./docs/configuration.md) | Plugin settings under `PLUGINS_CONFIG` |
| [Integrations](./docs/integrations.md) | The BGP Sessions tabs added to core NetBox objects |
| [Branching](./docs/branching.md) | Using the plugin with netbox-branching |
| [Data Model](./docs/models/bgpsession.md) | Field reference for each model |
| [REST API](./docs/rest-api.md) | Endpoints, including the backwards-compatible aliases |
| [GraphQL API](./docs/graphql-api.md) | Query fields and an example query |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development environment, test workflow,
and release conventions.
