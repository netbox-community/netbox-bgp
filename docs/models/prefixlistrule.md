# Prefix List Rules

A single entry in a [Prefix List](./prefixlist.md), permitting or denying one prefix, with
optional `ge` and `le` length qualifiers.

## Fields

### Prefix List

**Required.** The parent list. Deleting the list deletes its rules.

### Index

**Required.** A positive integer giving the rule's position within the list. Unique per
list, and the field rules are ordered by.

### Action

**Required.** One of:

| Value    | Label  |
|----------|--------|
| `permit` | Permit |
| `deny`   | Deny   |

### Prefix and Prefix Custom

The network the rule matches, given one of two ways:

* **Prefix** — a foreign key to an existing `ipam.Prefix`, keeping the rule linked to a
  prefix NetBox already tracks.
* **Prefix Custom** — a free-form network literal, for a prefix that is not (and need not
  be) recorded in IPAM, such as `0.0.0.0/0`.

**Set exactly one.** Setting both, or neither, is rejected.

The read-only **`network`** property returns whichever is populated, so consumers do not
have to check both. It prefers Prefix Custom when — contrary to validation — both somehow
hold a value.

!!! note
    Prefix Custom is stored as a network object rather than a string, so a value written as
    `10.0.0.0/8` is read back in normalised form.

### GE and LE

Optional prefix-length qualifiers, each an integer between 0 and 128 — the IPv6 maximum,
applied regardless of the parent list's [family](./prefixlist.md#family).

The plugin does not check that `ge` ≤ `le`, that either exceeds the prefix's own length, or
that they fall within the family's valid range.

### Description

An optional description, up to 200 characters.

!!! note
    This model has no bulk edit view in the UI.
