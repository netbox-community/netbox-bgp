# Community Lists

A named container of [Community List Rules](./communitylistrule.md), equivalent to a
community-list in vendor configuration. Referenced by
[Routing Policy Rules](./routingpolicyrule.md) through their Match Community List field.

## Fields

### Name

**Required.** The list's name, up to 100 characters.

### Description

An optional description, up to 200 characters. Name and description together must be
unique.

## Rules

A community list has no configuration of its own beyond its name — its behaviour comes
entirely from its rules. Rules are ordered by the community they reference, and are deleted
along with the list.

!!! note
    Unlike [Prefix List Rules](./prefixlistrule.md) and
    [AS Path List Rules](./aspathlistrule.md), community list rules have no `index` field.
    They are ordered by community value rather than by an explicit sequence number.
