# AS Path Lists

A named container of ordered [AS Path List Rules](./aspathlistrule.md), equivalent to an
as-path access-list or as-path filter. Referenced by
[Routing Policy Rules](./routingpolicyrule.md#match-as-path-list) through their Match AS
Path List field.

## Fields

### Name

**Required.** The list's name, up to 100 characters.

### Description

An optional description, up to 200 characters. Name and description together must be
unique.
