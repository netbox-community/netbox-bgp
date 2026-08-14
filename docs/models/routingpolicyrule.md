# Routing Policy Rules

A single term within a [Routing Policy](./routingpolicy.md), pairing a set of match
conditions with an action and a set of values to set. This is the plugin's richest rule
model, and the only one whose matches span several object types.

## Fields

### Routing Policy

**Required.** The parent policy. Deleting the policy deletes its rules.

### Index

**Required.** A positive integer giving the rule's position within the policy. Unique per
policy, and the field rules are ordered by.

### Action

**Required.** One of:

| Value    | Label  |
|----------|--------|
| `permit` | Permit |
| `deny`   | Deny   |

### Continue Entry

An optional positive integer, recording a `continue` statement's target index for platforms
that support falling through to a later term.

### Match Community

Many-to-many references to [Communities](./community.md) the rule matches directly.

### Match Community List

Many-to-many references to [Community Lists](./communitylist.md).

!!! warning
    When a rule has both direct communities and community lists, the generated match
    statement uses the **community lists only** — the lists overwrite the direct
    communities rather than being combined with them. Use one or the other on a given rule.

### Match AS Path List

Many-to-many references to [AS Path Lists](./aspathlist.md).

### Match IP Address and Match IPv6 Address

Many-to-many references to [Prefix Lists](./prefixlist.md), for IPv4 and IPv6 matches
respectively. The plugin does not check that the referenced list's
[family](./prefixlist.md#family) agrees with the field it is attached to.

### Match Custom

An optional free-form JSON object for match conditions the plugin does not model. Keys it
does not share with a modelled match are passed through unchanged.

!!! warning
    For the four keys that *do* overlap — `community`, `ip address`, `ipv6 address`, and
    `as-path` — a value in Match Custom **replaces** the modelled match rather than adding
    to it. Setting `{"community": ["65001:1"]}` on a rule that also has Match Community
    entries drops those entries from the derived
    [`match_statements`](#derived-values). Keep custom keys disjoint from the modelled
    fields, or put all of a given match type in one place.

### Set Actions

An optional free-form JSON object holding the rule's `set` statements. Stored and returned
as-is; no schema is enforced.

### Description

An optional description, up to 500 characters — longer than the 200 allowed on most other
models.

## Derived Values

Two read-only properties assemble the rule for consumption by templating or automation:

* **`match_statements`** assembles the modelled matches keyed by vendor term (`community`,
  `ip address`, `ipv6 address`, `as-path`), drops the empty ones, then overlays
  `match_custom` — see the warning above for what that overlay does to overlapping keys.
* **`set_statements`** returns `set_actions`, or an empty object when it is unset.

!!! note
    This model has no bulk edit view in the UI.
