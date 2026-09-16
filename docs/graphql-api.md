# GraphQL API

The plugin extends NetBox's GraphQL schema, served at `/graphql/`. Each model provides a
single-object field and a `_list` field.

## Query Fields

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

!!! warning
    Note the two similar-looking names. `netbox_bgp_community_list` is the list of
    **Communities**, whereas the Community List model is queried via
    `netbox_bgp_communitylist` / `netbox_bgp_communitylist_list`.

These field names are load-bearing for existing clients and will not be renamed.

## Example

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

## Nullable Remote Address

`BGPSessionType.remote_address` is nullable (`IPAddressType | None`), because a session may
carry a [Remote Prefix](./models/bgpsession.md#remote-prefix) instead of a single address.
The `remote_prefix` field is likewise nullable. A query that selects both and falls back
between them handles either shape:

```graphql
query {
  netbox_bgp_session_list {
    id
    remote_address { address }
    remote_prefix { prefix }
  }
}
```

!!! note
    `remote_address` became nullable in 0.20.0. Clients written against earlier releases
    that assume the field is always present must be updated.
