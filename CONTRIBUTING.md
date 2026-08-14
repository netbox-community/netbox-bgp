# Contributing

Thanks for contributing to `netbox-bgp`. This document covers the development
environment, the test workflow, and the conventions to follow when adding to the plugin.

## Requirements

* Docker with Compose v2 (`docker compose`, not `docker-compose`)
* GNU Make

Everything runs inside a Docker Compose stack, so no local Python environment or
PostgreSQL install is needed.

## Branches

Development happens on `develop`. Branch from `develop` and open pull requests against
it. Release branches (`release-X.Y.Z`) are cut from `develop`.

## Development environment

`develop/` contains a Compose stack (NetBox + worker + PostgreSQL + Redis). The plugin
source is bind-mounted into the NetBox container, so edits on the host apply after a
container restart, or immediately under `runserver` autoreload.

Always drive the stack through `make` rather than raw `docker compose`, so the project
name and compose file stay consistent.

| Command | What it does |
|---|---|
| `make cbuild` | Build the dev image |
| `make debug` | Run the stack in the foreground |
| `make start` | Run the stack detached |
| `make stop` | Stop the stack |
| `make destroy` | Stop the stack **and drop the PostgreSQL volume** |
| `make adduser` | Create a superuser |
| `make nbshell` / `make shell` | NetBox shell / Django shell |
| `make migrations` | Generate migrations for the plugin |
| `make test` | Build the image, then run the test suite |
| `make update-query-counts` | Regenerate the query-count baselines (see below) |
| `make collectstatic` | Run `collectstatic` |

To target a different NetBox version or Python version, override the build args — the
defaults live at the top of the `Makefile`:

```
make cbuild NETBOX_VER=v4.7.0 PYTHON_VER=3.12
```

Use `make destroy` when migrations get wedged; it drops the database volume so the next
start applies migrations from scratch.

## Tests

```
make test
```

This builds the image and runs `python manage.py test netbox_bgp` inside the container.
To run a single test:

```
docker compose -f develop/docker-compose.yml -p netbox_bgp run netbox \
  python manage.py test netbox_bgp.tests.test_api.SomeTestCase.test_method
```

Tests live in `netbox_bgp/tests/`, mirroring the structure of the plugin:

| File | Covers |
|---|---|
| `test_models.py` | `__str__`, `clean()` validation, property logic, constraints |
| `test_api.py` | REST API and GraphQL, via NetBox's `APIViewTestCases` |
| `test_views.py` | UI views, via NetBox's `ViewTestCases` |
| `test_filtersets.py` | FilterSet `search()` and explicit filter fields |
| `test_forms.py` | Form logic not exercised by the view tests |
| `test_search.py` | `SearchIndex` registration and cached fields |

Most of the test count comes from NetBox's base classes rather than explicit `test_*`
methods, so adding a model to a `ViewTestCases`/`APIViewTestCases` subclass pulls in a
large amount of coverage for free.

### Query-count baselines

NetBox asserts that list views execute a known number of SQL queries, using per-app
baselines committed at `netbox_bgp/tests/query_counts.json`. A test fails if the recorded
key is missing or the count has changed.

If you add a model with a list view, or change prefetching, serializers, or table
columns in a way that moves the query count, regenerate the baselines and commit the
result:

```
make update-query-counts
```

This runs the suite with `UPDATE_QUERY_COUNTS=1`, which records observed counts instead
of asserting them. It must run serially — the update mode refuses to run under
`--parallel`. Review the diff before committing: an unexpected jump usually means an
N+1 was introduced rather than that the baseline was stale.

## Migrations

Never hand-write migrations. After any change to `models.py`:

```
make migrations
```

This runs `makemigrations` inside the container and writes into
`netbox_bgp/migrations/`. Commit the generated file with the model change.

## Adding a model

A model has to be wired through every layer, or the UI, REST API, GraphQL, or global
search will be silently incomplete. Add it to all of:

`models.py`, `forms.py`, `tables.py`, `filtersets.py`, `api/serializers.py`,
`api/views.py`, `api/urls.py`, `graphql/types.py`, `graphql/filters.py`,
`graphql/schema.py`, `navigation.py`, `urls.py`, `search.py` (if it should be
searchable), `templates/netbox_bgp/<name>.html`, a migration, and tests.

Two conventions that are easy to miss:

* GraphQL filter classes are declared with a `NetBoxBGP` prefix to keep type names
  unique in the shared schema, but NetBox discovers a model's filter at the conventional
  `netbox_bgp.graphql.filters.<Model>Filter` path. Add an alias at the bottom of
  `graphql/filters.py` alongside the existing ones, or the GraphQL filter tests will
  fail for the new model.
* Several models set `verbose_name_plural` explicitly (`Communities`, `Community Lists`,
  `Routing Policies`, `Peer Groups`, `Prefix Lists`, `AS Path Lists`, `BGP Sessions`)
  because Django's default pluraliser gets them wrong. Preserve these when editing
  `Meta`.

See [CLAUDE.md](CLAUDE.md) for a fuller description of the architecture and the
test-suite quirks.

## Coding standards

The plugin follows NetBox core's conventions:

* Mirror the patterns used by existing models rather than introducing new ones.
* Models exposed in the UI inherit from `NetBoxModel`, which provides change logging,
  tags, custom fields, and journaling.
* API serializers include a `url` field.
* List and API views generally don't need `select_related()` / `prefetch_related()` —
  prefetching is derived from the table and serializer.
* Don't run `ruff format` across existing files; it produces large unrelated diffs.
* Avoid new dependencies without strong justification.

## Compatibility and releases

The version string has a single home: `netbox_bgp/version.py`, read by both `setup.py`
and `PluginConfig`.

The NetBox ⇄ plugin version pairing is strict, and it is recorded in three places that
must be kept in step:

1. `min_version` / `max_version` in `netbox_bgp/__init__.py`
2. The table in `COMPATIBILITY.md`
3. The `compatibility` list in `netbox-plugin.yaml`

Changing the supported NetBox range usually also means migrations and adjustments to
imports from NetBox internals.

`make relpatch` bumps the patch version on a release branch; it requires a clean working
tree. `make pbuild` builds the sdist and wheel, and `make pypipub` uploads to PyPI.

If you add non-Python files that need to ship in the package, add them to `MANIFEST.in`
— `setup.py` uses `include_package_data`, which has nothing to include without it.
