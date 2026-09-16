# Communities

A BGP community — a tag attached to routes and matched by policy. Communities are
referenced by [Community List Rules](./communitylistrule.md) and directly by
[Routing Policy Rules](./routingpolicyrule.md).

## Fields

### Value

**Required.** The community value, up to 64 characters, in `<part>:<part>` form. Each part
may contain digits, dots, and the `*` wildcard, so both plain values (`65001:100`) and
patterns (`65001:*`) are accepted.

!!! note
    The validation is a loose, unanchored pattern match rather than a semantic check. It
    requires only that a `<digits/dots/asterisks>:<digits/dots/asterisks>` sequence appear
    *somewhere* in the value, so surrounding text is accepted, and it does not verify that
    the parts fall within valid ranges.

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
