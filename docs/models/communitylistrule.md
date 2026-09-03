# Community List Rules

A single entry in a [Community List](./communitylist.md), permitting or denying one
[Community](./community.md).

## Fields

### Community List

**Required.** The parent list. Deleting the list deletes its rules.

### Community

**Required.** The [Community](./community.md) this rule matches. Deleting the community
deletes any rule referencing it.

### Action

**Required.** One of:

| Value    | Label  |
|----------|--------|
| `permit` | Permit |
| `deny`   | Deny   |

### Description

An optional description, up to 200 characters.

## Ordering

Rules are ordered by parent list, then by community. There is no `index` field on this
model — see the [note on Community Lists](./communitylist.md#rules).

!!! note
    This model has neither a bulk edit nor a bulk import view in the UI. Rules are managed
    individually, or through the [REST API](../rest-api.md).
