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

An optional free-form JSON object for match conditions the plugin does not model, such as
`{"extcommunity": ["rt:65000:1"]}`. Keys it does not share with a modelled match are passed
through unchanged.

For the four keys that *do* overlap — `community`, `ip address`, `ipv6 address`, and
`as-path` — the custom values are added to the modelled ones. A rule with a Match Community
of `65000:100` and a Match Custom of `{"community": ["65000:200"]}` yields both in the
derived [`match_statements`](#derived-values).

!!! note
    Prior to 0.20.0 a custom value under one of those four keys silently *replaced* the
    modelled match instead of adding to it. If you worked around that by duplicating
    modelled matches into Match Custom, those entries will now appear twice.

### Set Actions

An optional free-form JSON object holding the rule's `set` statements. Stored and returned
as-is; no schema is enforced.

### Description

An optional description, up to 500 characters — longer than the 200 allowed on most other
models.

## Derived Values

Two read-only properties assemble the rule for consumption by templating or automation:

* **`match_statements`** assembles the modelled matches keyed by vendor term (`community`,
  `ip address`, `ipv6 address`, `as-path`), merges in the matching keys from
  `match_custom`, adds any unmodelled custom keys, and drops whatever is left empty.
* **`set_statements`** returns `set_actions`, or an empty object when it is unset.

!!! note
    This model has no bulk edit view in the UI.
