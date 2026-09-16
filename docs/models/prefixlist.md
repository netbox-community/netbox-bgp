# Prefix Lists

A named container of ordered [Prefix List Rules](./prefixlistrule.md). Prefix lists are
referenced by [BGP Sessions](./bgpsession.md#prefix-list-in-and-out) and
[Peer Groups](./bgppeergroup.md#prefix-list-in-and-out) for inbound and outbound
filtering, and by [Routing Policy Rules](./routingpolicyrule.md#match-ip-address-and-match-ipv6-address)
as match conditions.

## Fields

### Name

**Required.** The list's name, up to 100 characters.

### Family

**Required.** The address family of the list. One of:

| Value  | Label |
|--------|-------|
| `ipv4` | IPv4  |
| `ipv6` | IPv6  |

!!! note
    Family is recorded on the list, not on its rules, and it is not enforced against them.
    Nothing prevents an IPv6 prefix from being added to a list marked IPv4, or an IPv4 list
    from being used as a rule's Match IPv6 Address.

### Description

An optional description, up to 200 characters. Name, description, and family together must
be unique — so the same name may be reused across the two families.
