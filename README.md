# Netbox BGP Plugin
[Netbox](https://github.com/netbox-community/netbox) plugin for BGP related objects documentation.

## Compatibility

This plugin in compatible with [NetBox](https://netbox.readthedocs.org/) 3.0.0 and later.
You can use older Netbox version with 0.3.9 version of this plugin.

## Installation

The plugin is available as a Python package in pypi and can be installed with pip  
For NetBox 2.10 or 2.11: 
```
pip install netbox-bgp==0.3.9
```
For NetBox 3.0: 
```
pip install netbox-bgp
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_bgp']
```
Restart NetBox and add `netbox-bgp` to your local_requirements.txt

## Configuration

The following options are available:
* `device_ext_page`: String (default right) Device related BGP sessions table position. The following values are available:  
left, right, full_width. Set empty value for disable.   
* `asdot`: Boolean (defaul False) asdot notation for 4-byte AS

## Screenshots

BGP Session Object
![BGP Session](docs/img/bgp_sess.png)

BGP Session Table
![BGP Session Table](docs/img/bgp_sess_list.png)

Device Extension
![Device Session Table](docs/img/dev_sess_list.png)

ASN Object
![ASN](docs/img/asn.png)

ASN Table
![ASN Table](docs/img/asn_list.png)

Community Object
![Community](docs/img/commun.png)
