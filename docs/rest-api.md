# REST API

All endpoints are served under `/api/plugins/bgp/`. Each behaves like any other NetBox REST
endpoint: list and detail views, filtering via query parameters, bulk create and update,
and brief mode.

## Endpoints

| Endpoint | Model |
|---|---|
| `session/` (alias: `bgpsession/`) | [BGP Session](./models/bgpsession.md) |
| `peer-group/` (alias: `bgppeergroup/`) | [Peer Group](./models/bgppeergroup.md) |
| `community/` | [Community](./models/community.md) |
| `community-list/` | [Community List](./models/communitylist.md) |
| `community-list-rule/` | [Community List Rule](./models/communitylistrule.md) |
| `routing-policy/` | [Routing Policy](./models/routingpolicy.md) |
| `routing-policy-rule/` | [Routing Policy Rule](./models/routingpolicyrule.md) |
| `prefix-list/` | [Prefix List](./models/prefixlist.md) |
| `prefix-list-rule/` | [Prefix List Rule](./models/prefixlistrule.md) |
| `aspath-list/` | [AS Path List](./models/aspathlist.md) |
| `aspath-list-rule/` | [AS Path List Rule](./models/aspathlistrule.md) |

## Legacy Aliases

Sessions and peer groups are each registered under two paths. The `session/` and
`peer-group/` spellings are preferred; `bgpsession/` and `bgppeergroup/` are retained for
backwards compatibility and serve the identical viewset, so existing integrations keep
working.

!!! note
    The aliases are not deprecated and will not be removed without a deprecation cycle.
    There is no behavioural difference between the two spellings — they resolve to the same
    objects and accept the same filters.

## Creating a Session

A session requires `local_address`, `local_as`, `remote_as`, and exactly one of
`remote_address` or `remote_prefix`:

```
curl -X POST \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  https://netbox/api/plugins/bgp/session/ \
  --data '{
    "name": "peering-01",
    "device": 12,
    "local_address": 401,
    "local_as": 7,
    "remote_address": 402,
    "remote_as": 8,
    "status": "active"
  }'
```

!!! warning
    `remote_address` is not a required field, because a session may carry a
    [Remote Prefix](./models/bgpsession.md#remote-prefix) instead. Supplying neither is
    rejected, and so is supplying both. Responses may contain `"remote_address": null` for
    prefix-based sessions, so clients must handle that case.

Unlike the **Add Session** form, the REST API never auto-creates an `ipam.IPAddress`. Both
`remote_address` and `remote_prefix` must reference objects that already exist, regardless
of the [`remote_address_strict`](./configuration.md#remote_address_strict) setting.
