# Routing Policies

A named container of ordered [Routing Policy Rules](./routingpolicyrule.md) — the plugin's
equivalent of a route-map. Routing policies are referenced by
[BGP Sessions](./bgpsession.md#import-and-export-policies) and
[Peer Groups](./bgppeergroup.md#import-and-export-policies) as import or export
policies.

## Fields

### Name

**Required.** The policy's name, up to 100 characters.

### Description

An optional description, up to 200 characters. Name and description together must be
unique.

### Weight

An optional positive integer. Policies are ordered by weight first, then by name, so this
controls where a policy appears in list views and selectors. It has no effect on how the
policy's own rules are evaluated — that is governed by each rule's
[index](./routingpolicyrule.md#index).

!!! note
    Weight is nullable, and PostgreSQL sorts nulls last on an ascending sort, so policies
    without a weight appear *after* those with one.
