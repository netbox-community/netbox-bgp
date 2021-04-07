# Netbox BGP Plugin
[Netbox](https://github.com/netbox-community/netbox) plugin for BGP related objects documentation.

## Compatibility

This plugin in compatible with [NetBox](https://netbox.readthedocs.org/) 2.10 and later.

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

## Configuration

The plugin is not configurable

## Screenshots

BGP Session Object
![BGP Session](docs/img/bgp_sess.png)

BGP Session Table
![BGP Session Table](docs/img/bgp_sess_list.png)

ASN Object
![ASN](docs/img/asn.png)

ASN Table
![ASN Table](docs/img/asn_list.png)

Community Object
![Community](docs/img/commun.png)