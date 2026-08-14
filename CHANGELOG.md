# Changelog

All notable changes to this project are documented in this file.

This changelog starts at 0.20.0. For earlier releases, see the
[compatibility matrix](COMPATIBILITY.md) and the git history.

## 0.20.0

**Requires NetBox 4.7.** This release drops support for NetBox 4.6 and earlier; see
[Upgrading](#upgrading-to-0200) below.

### Added

- **Prefixes as remote peers** ([#282](https://github.com/netbox-community/netbox-bgp/issues/282)).
  A BGP Session can now nominate an `ipam.Prefix` as its remote peer via the new
  **Remote Prefix** field, documenting dynamic peering — where a device accepts sessions
  from any address within a subnet (`bgp listen range` on Cisco/Arista, `allow` on
  Juniper). Previously this had to be faked by creating a placeholder IP address.

  Set **exactly one** of Remote Address or Remote Prefix; setting both, or neither, is
  rejected in the UI, the REST API, and bulk import. The field is available in the edit,
  add, and import forms, as a table column, in the REST API and GraphQL, and as the
  filters `remote_prefix`, `remote_prefix_id`, and `by_remote_prefix`.

  Unlike Remote Address, a Remote Prefix is never auto-created — the Prefix must already
  exist, regardless of the `remote_address_strict` setting.

- **BGP Sessions tab on Prefix**, listing sessions whose Remote Prefix is that prefix.
  This is the eighth core-object integration; the full set is documented in the README.

- **`make update-query-counts`** — records the SQL query-count baselines that NetBox
  4.7's test framework asserts against, into `netbox_bgp/tests/query_counts.json`. Must
  be run serially. Regenerate and commit this file whenever a change affects
  prefetching. See `CONTRIBUTING.md`.

- **`CONTRIBUTING.md`** — development workflow, `make` targets, test conventions, the
  query-count baseline workflow, and the add-a-model checklist.

- Substantially expanded **README**: the seven (now eight) core-object integrations, the
  REST endpoint table including the backwards-compatible aliases, the GraphQL query
  fields, and the previously undocumented `extra_attributes`, `remote_as_macro`, and
  peer-group defaults behaviour.

### Changed

- **NetBox 4.7 support.** `max_version` is now `4.7.99`. The development stack targets
  NetBox's `feature` branch (`NETBOX_VER?=feature`).

- **List view actions migrated to NetBox 4.7's object-actions API.** The dict form
  (`actions = {'add': {'add'}, ...}`) is replaced by action classes
  (`actions = (AddObject, BulkImport, BulkExport, BulkDelete)`) on the
  CommunityListRule, RoutingPolicyRule, PrefixListRule, and ASPathListRule list views.

- **GraphQL filter aliases.** Each filter class is now also exported under the
  conventional `<Model>Filter` name (`BGPSessionFilter`, `CommunityFilter`, …) alongside
  the existing `NetBoxBGP*` names, which NetBox 4.7 requires in order to discover a
  model's filter class. The GraphQL schema itself is unchanged — type names are taken
  from the decorated class — so no client changes are needed.

- `MANIFEST.in` now ships `netbox_bgp/tests/*.json`, so the query-count baselines are
  included in the built distribution.

### Breaking changes

- **GraphQL: `BGPSessionType.remote_address` is now nullable.** It changes from
  `IPAddressType` to `IPAddressType | None`, because a session may now carry a Remote
  Prefix instead. Clients that rely on the field being non-null must handle `null`.
  The new `remote_prefix` field is likewise nullable.

- **REST: `remote_address` is no longer a required field** on `BGPSessionSerializer`
  (`required=False, allow_null=True`). This only relaxes writes — existing clients that
  always send `remote_address` are unaffected — but responses may now contain
  `"remote_address": null` for prefix-based sessions.

- **NetBox 4.6 and earlier are no longer supported.**

### Upgrading to 0.20.0

1. Upgrade NetBox to 4.7 first, following the
   [NetBox upgrade instructions](https://netboxlabs.com/docs/netbox/installation/upgrading/).
   NetBox 4.7 has its own PostgreSQL, Redis, and Python floors — check its release notes.
2. Upgrade the plugin: `pip install --upgrade netbox-bgp`
3. Run migrations: `python manage.py migrate`

Migration `0042` adds the `remote_prefix` column, makes `remote_address` nullable, and
adds two conditional unique constraints covering prefix-based sessions. No data is
modified: existing sessions keep their Remote Address and are unaffected.

Review any GraphQL clients for the `remote_address` nullability change before upgrading.
