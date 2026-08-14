# Peer Groups

A peer group collects settings shared by several BGP sessions, mirroring the peer-group
construct found in most vendor implementations. Sessions reference a group through their
[Peer Group](./bgpsession.md#peer-group) field.

## Fields

### Name

**Required.** The group's name, up to 100 characters.

### Description

An optional description, up to 200 characters. Name and description together must be
unique.

### Local AS and Remote AS

Optional `ipam.ASN` references describing the AS numbers the group's sessions use. Both are
cleared to null if the ASN is deleted.

### Import and Export Policies

Many-to-many references to [Routing Policies](./routingpolicy.md) that the group's sessions
are expected to apply.

### Prefix List In and Out

Optional [Prefix Lists](./prefixlist.md) for filtering in each direction.

### Extra Attributes

A free-form JSON object for configuration data the plugin does not model explicitly, stored
and returned as-is with no schema enforced. Defaults to an empty object.

## Defaults Are Not Inherited

A peer group's `local_as`, `remote_as`, prefix lists, policies, and `extra_attributes`
describe group-wide defaults **for your own tooling to apply**. The plugin does not merge
them into the sessions that reference the group.

!!! warning
    A session's `import_policies` and `export_policies`, in both the UI and the REST API,
    are always the session's own policies — never the union with its peer group's. The same
    is true of the AS numbers, prefix lists, and extra attributes. If you need the
    group-level values, read the peer group explicitly.

This is a deliberate modelling choice rather than an oversight: it keeps a session's stored
data equal to its reported data, so an API consumer never has to know which values were
inherited and which were set directly. The cost is that resolving the effective
configuration is the consumer's job.
