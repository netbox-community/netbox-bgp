# Community List Rules

A single entry in a [Community List](./communitylist.md), permitting or denying one
[Community](./community.md).

## Fields

### Community List

**Required.** The parent list. Deleting the list deletes its rules.

### Community and Community Custom

The community the rule matches, given one of two ways:

* **Community** — a foreign key to an existing [Community](./community.md), keeping the
  rule linked to a community NetBox already tracks. Deleting the community deletes any
  rule referencing it.
* **Community Custom** — a free-form string, for anything that isn't a literal
  `ASN:VALUE` community NetBox can model directly — most commonly a regular expression
  (e.g. `^65001:.*$`), for vendors whose community-list syntax supports regex/expanded
  matching (such as Cisco IOS `ip community-list expanded`).

**Set exactly one.** Setting both, or neither, is rejected.

The read-only **`value`** property returns whichever is populated, so consumers do not
have to check both. It prefers Community Custom when — contrary to validation — both
somehow hold a value.

Note that NetBox itself does not interpret Community Custom as a regular expression; the
plugin treats it as an opaque string carried through to generated configuration. Any
regex syntax is meaningful only to the target vendor's community-list implementation.

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
