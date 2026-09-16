# Integrations with Core NetBox Objects

In addition to its own list and detail views, the plugin adds a **BGP Sessions** tab to
several core NetBox objects. Each tab lists the sessions related to the object you are
viewing, so you can reach the BGP configuration from the device, address, or tenant you
already have open rather than filtering the session list by hand.

## Available Tabs

| Object          | Sessions shown                                                            |
|-----------------|---------------------------------------------------------------------------|
| Device          | Sessions whose Device is this device                                      |
| Virtual Machine | Sessions whose Virtual Machine is this VM                                 |
| Interface       | Sessions whose local or remote address is an IP assigned to this interface |
| IP Address      | Sessions whose local **or** remote address is this IP                     |
| ASN             | Sessions whose local **or** remote AS is this ASN                         |
| Prefix          | Sessions whose Remote Prefix is this prefix                               |
| Site            | Sessions whose Site is this site                                          |
| Tenant          | Sessions whose Tenant is this tenant                                      |

Note that the IP Address and ASN tabs match on either end of the session. A session appears
under both its local and its remote address, and under both its local and its remote AS.

## The Device Tab

All of these tabs are enabled by default except the Device one, which is controlled by the
[`device_ext_page`](./configuration.md#device_ext_page) setting. Set it to `tab` for a
dedicated tab, or use `left`, `right`, or `full_width` to render the sessions inline on the
device page instead. Setting it to an empty string disables the device display entirely.

!!! warning
    `device_ext_page` is read when the plugin is loaded, so changing it requires a NetBox
    and worker restart.

## The Prefix Tab

The Prefix tab lists sessions whose **Remote Prefix** is that prefix — that is, sessions
documenting dynamic peering into the subnet. It does not list sessions whose remote
*address* happens to fall within the prefix. See
[BGP Session: Remote Prefix](./models/bgpsession.md#remote-prefix).
