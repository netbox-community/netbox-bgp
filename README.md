# NetBox BGP Plugin
[Netbox](https://github.com/netbox-community/netbox) plugin for BGP related objects documentation.

## Features
This plugin provide following Models:
* BGP Communities
* BGP Sessions
* Routing Policy
* Prefix Lists 

## Compatibility

|             |       |
|-------------|-------|
| NetBox 2.10 | 0.3.9 |
| NetBox 2.11 | 0.3.9 |
| NetBox 3.0  | 0.4.3 |
| NetBox 3.1  | 0.5.0 |
| NetBox 3.2  | >= 0.6.0 |
| NetBox 3.3  | >= 0.8.1 |

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
* `device_ext_page`: String (default right) Device related BGP sessions table position. The following values are available:  
left, right, full_width. Set empty value for disable.

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