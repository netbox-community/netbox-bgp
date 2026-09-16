# AS Path List Rules

A single entry in an [AS Path List](./aspathlist.md), permitting or denying AS paths that
match a regular expression.

## Fields

### AS Path List

**Required.** The parent list. Deleting the list deletes its rules.

### Index

**Required.** A positive integer giving the rule's position within the list, and the field
rules are ordered by.

!!! note
    Unlike [Prefix List Rules](./prefixlistrule.md#index) and
    [Routing Policy Rules](./routingpolicyrule.md#index), the index is **not** constrained
    to be unique per list. Two rules in the same AS path list may share an index, in which
    case their relative order is undefined.

### Action

**Required.** One of:

| Value    | Label  |
|----------|--------|
| `permit` | Permit |
| `deny`   | Deny   |

### Pattern

**Required.** The AS path regular expression, up to 200 characters — for example
`^65001_` or `_65002$`.

!!! warning
    The pattern is stored verbatim as a label. The plugin does not compile it, validate it,
    or evaluate it against anything, and regex syntax varies between vendors. An invalid
    expression will be accepted here and only fail when your tooling applies it.

### Description

An optional description, up to 200 characters.

!!! note
    This model has no bulk edit view in the UI.
