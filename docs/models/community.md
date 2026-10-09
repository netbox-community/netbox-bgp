# Communities

A BGP community — a tag attached to routes and matched by policy. Communities are
referenced by [Community List Rules](./communitylistrule.md) and directly by
[Routing Policy Rules](./routingpolicyrule.md).

## Fields

### Value

**Required.** The community value, up to 64 characters, in `<part>:<part>` form. Each part
may contain digits, dots, the `*` wildcard, `\d`, and bracket expressions such as `[0-9]` or
`[^0-9]`. Any of these may be followed by a quantifier (`+`, `?`, `{n}` or `{n,m}`). Plain
values and patterns are both accepted:

| Example                       | Meaning                          |
|-------------------------------|----------------------------------|
| `65001:100`                   | Plain community                  |
| `65001:*`                     | Wildcard                         |
| `64522:123[0-9]`              | Digit range                      |
| `64522:[0-9][0-9][0-9][0-9]`  | Any four-digit value             |
| `64522:[0-9]{4}`              | Same, using a quantifier         |

!!! note
    The validation is a loose, unanchored pattern match rather than a semantic check. It
    requires only that a `<part>:<part>` sequence of the characters above appear
    *somewhere* in the value, so surrounding text is accepted, and it does not verify that
    the parts fall within valid ranges or that the pattern is a complete, valid regex.

### Status

The community's lifecycle state. One of:

| Value        | Label      |
|--------------|------------|
| `active`     | Active     |
| `reserved`   | Reserved   |
| `deprecated` | Deprecated |

Defaults to Active.

### Role

An optional `ipam.Role`, reusing NetBox's own role objects to classify the community.

### Site and Tenant

Optional `dcim.Site` and `tenancy.Tenant` assignments. Both are protected: the site or
tenant cannot be deleted while a community references it.

### Description

An optional description, up to 200 characters.

## Ordering

Communities are ordered by value. Unlike most other models in the plugin, there is no
uniqueness constraint on the value — the same community may be recorded more than once, for
example under different tenants.
