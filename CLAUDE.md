# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`netbox-bgp` is a [NetBox](https://github.com/netbox-community/netbox) plugin that adds BGP-related objects (Sessions, Peer Groups, Communities, Community Lists, Routing Policies + Rules, Prefix Lists + Rules, AS Path Lists + Rules). The plugin is distributed on PyPI as `netbox-bgp` and installs as a Django app named `netbox_bgp`.

The NetBox ⇄ plugin version pairing is strict (declared in `netbox_bgp/__init__.py` via `min_version`/`max_version` and summarised in `README.md`). The current branch (`0.19.0`) targets NetBox 4.5.x. Changing the plugin's NetBox version range almost always requires migrations and import changes against NetBox internals.

## Development workflow

The `develop/` directory contains a full Docker Compose stack (NetBox + worker + Postgres + Redis). The plugin source is bind-mounted into the NetBox container, so edits on the host take effect after a container restart (or `runserver` autoreload). The `Makefile` wraps everything — prefer it over raw `docker compose`.

Common commands (all run via `make`):

- `make cbuild` — build the dev image. Pass `NETBOX_VER=vX.Y.Z PYTHON_VER=3.12` to target a different NetBox tag.
- `make debug` / `make start` / `make stop` — run the stack in foreground / detached / stop.
- `make destroy` — stop the stack **and drop the Postgres volume** (`netbox_bgp_pgdata_netbox_bgp`). Use when migrations get wedged.
- `make migrations` — generate Django migrations for the plugin (writes into `netbox_bgp/migrations/`). Required after any `models.py` change.
- `make test` — run `python manage.py test netbox_bgp` inside the container. Tests live in `netbox_bgp/tests/` (`test_api.py`, `test_forms.py`, `test_models.py`, `test_views.py`). Run a single test with: `docker compose -f develop/docker-compose.yml -p netbox_bgp run netbox python manage.py test netbox_bgp.tests.test_api.SomeTestCase.test_method`.
- `make nbshell` / `make shell` — NetBox shell / Django shell.
- `make adduser` — create a superuser.
- `make pbuild` / `make pypipub` — build sdist/wheel / upload to PyPI.
- `make relpatch` — bump patch version on a release branch (requires clean working tree; runs `pysemver bump patch` against `netbox_bgp/version.py`).

The version string lives in a single place: `netbox_bgp/version.py` (read by both `setup.py` and `PluginConfig`).

## Architecture

This is a standard NetBox plugin — `netbox_bgp/__init__.py` exposes a `PluginConfig` subclass as `config`, which NetBox discovers when the plugin is listed in `PLUGINS`. Everything else follows NetBox's plugin conventions; when adding features, mirror the patterns used by existing models rather than inventing new ones.

### Models (`netbox_bgp/models.py`)

All models inherit from `netbox.models.NetBoxModel` (giving them change-logging, tags, custom fields, journaling). Two shapes are used heavily:

- **List / Rule pairs**: `PrefixList` ↔ `PrefixListRule`, `CommunityList` ↔ `CommunityListRule`, `ASPathList` ↔ `ASPathListRule`, `RoutingPolicy` ↔ `RoutingPolicyRule`. Rules are ordered by `(parent, index)` and `on_delete=CASCADE` from the parent.
- **`BGPBase` abstract**: provides `site`, `tenant`, `status`, `role`, `description`, `comments`. Currently only `Community` inherits it; `BGPSession` is a standalone model with its own richer FK set (device/vm, local/remote IP + AS, peer group, import/export policies, prefix lists in/out, `remote_as_macro`).

`BGPSession.label` falls back to `f'{remote_address}:{remote_as}'` when `name` is unset — don't introduce code that assumes `name` is always populated. `BGPSession.Meta.unique_together` covers both device- and VM-scoped tuples; a session must have exactly one of device/VM in practice (the `clean()` enforcement is currently commented out — see `models.py:489`).

`PrefixListRule` has dual prefix fields: `prefix` (FK to `ipam.Prefix`) and `prefix_custom` (`IPNetworkField`). Exactly one must be set; this is enforced in `clean()`. The `network` property returns whichever is populated.

### Surface area (one module per concern)

- `api/` — DRF viewsets/serializers mounted via `NetBoxRouter`. Note: both `bgpsession`/`session` and `bgppeergroup`/`peer-group` are registered as aliases for backwards compatibility (`api/urls.py`). When adding endpoints, register both spellings only if you're preserving an alias; otherwise pick one.
- `graphql/` — strawberry-django schema, types, filters, enums. The top-level `NetBoxBGPQuery` type exposes `netbox_bgp_*` fields; field names are load-bearing for GraphQL clients.
- `filtersets.py` / `forms.py` / `tables.py` — FilterSets (django-filter), edit/filter/bulk forms, and django-tables2 tables.
- `urls.py` — uses `utilities.urls.get_model_urls()` (NetBox 4.x pattern) rather than hand-written URL patterns. `detail=False` mounts list/add/import; the `<int:pk>/` line mounts the detail subtree.
- `views.py` — model views. Registered via `get_model_urls()` discovery, not manual URL conf.
- `template_content.py` — registers extra tabs/pages on NetBox core objects (Device, Interface, Site, Tenant, VirtualMachine, ASN, IPAddress) using `register_model_view` + `ViewTab`. **Reads `PLUGINS_CONFIG['netbox_bgp']['device_ext_page']` at import time** to decide whether to register a Device tab; changing that config requires a restart. The Device-specific inline (`left`/`right`/`full_width`) uses a `PluginTemplateExtension` instead.
- `navigation.py` — menu items; honours `top_level_menu` setting.
- `templates/netbox_bgp/` — per-object detail templates.
- `migrations/` — 0001 through 0039 at time of writing. Always add new ones via `make migrations`, don't hand-write.

### Plugin settings

Defined in `BGPConfig.default_settings`:

- `device_ext_page` (default `"right"`): `"left"` / `"right"` / `"full_width"` / `"tab"` / `""` (disabled).
- `top_level_menu` (default `False`).

Access at runtime via `settings.PLUGINS_CONFIG['netbox_bgp']`.

## Architecture Conventions

Inherited from NetBox core (https://github.com/netbox-community/netbox/blob/main/CLAUDE.md) — this plugin follows the same conventions as a NetBox Django app:

- **Apps**: Each Django app owns its models, views, API serializers, filtersets, forms, and tests.
- **Views**: Use `register_model_view()` to register model views by action (e.g. "add", "list", etc.). List views typically don't need to add `select_related()` or `prefetch_related()` on their querysets: Prefetching is handled dynamically by the table class so that only relevant fields are prefetched.
- **REST API**: DRF serializers live in `<app>/api/serializers.py`; viewsets in `<app>/api/views.py`; URLs auto-registered in `<app>/api/urls.py`. REST API views typically don't need to add `select_related()` or `prefetch_related()` on their querysets: Prefetching is handled dynamically by the serializer so that only relevant fields are prefetched.
- **GraphQL**: Strawberry types in `<app>/graphql/types.py`.
- **Filtersets**: `<app>/filtersets.py` — used for both UI filtering and API `?filter=` params.
- **Tables**: `django-tables2` used for all object list views (`<app>/tables.py`).
- **Templates**: Django templates in `netbox/templates/<app>/` (in this plugin: `netbox_bgp/templates/netbox_bgp/`).
- **Tests**: Mirror the app structure in `<app>/tests/`. Use `netbox.configuration_testing` for test config.

## Coding Standards

Inherited from NetBox core:

- Follow existing Django conventions; don't reinvent patterns already present in the codebase.
- New models must include `created`, `last_updated` fields (inherit from `NetBoxModel` where appropriate).
- Every model exposed in the UI needs: model, serializer, filterset, form, table, views, URL route, and tests.
- API serializers must include a `url` field (absolute URL of the object).
- Use `FeatureQuery` for generic relations (config contexts, custom fields, tags, etc.).
- Avoid adding new dependencies without strong justification.
- Avoid running `ruff format` on existing files, as this tends to introduce unnecessary style changes.
- Don't craft Django database migrations manually: Prompt the user to run `make migrations` instead (which runs `manage.py makemigrations` inside the dev container).

## Conventions to preserve

- When adding a model, add it across **all** of: `models.py`, `forms.py`, `tables.py`, `filtersets.py`, `api/serializers.py`, `api/views.py`, `api/urls.py`, `graphql/types.py`, `graphql/filters.py`, `graphql/schema.py`, `navigation.py`, `urls.py`, `templates/netbox_bgp/<name>.html`, and a migration. Missing any of these breaks either the UI, REST API, or GraphQL.
- API URL registration keeps legacy aliases (`session` + `bgpsession`, `peer-group` + `bgppeergroup`). Don't remove them without a deprecation cycle — external tooling depends on these paths.
- Verbose plural names are set explicitly on several models (`Communities`, `Routing Policies`, `Peer Groups`, `Prefix Lists`, `AS Path Lists`) because Django's default pluraliser gets them wrong. Preserve these when editing `Meta`.
