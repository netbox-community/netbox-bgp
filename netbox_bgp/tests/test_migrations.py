from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class CommunitySiteToScopeMigrationTestCase(TransactionTestCase):
    """netbox_bgp 0044 -> 0045 must fold existing Community.site values into the
    new generic scope field before dropping the legacy column."""

    migrate_from = [("netbox_bgp", "0044_community_scope_id_community_scope_type")]
    migrate_to = [("netbox_bgp", "0045_remove_community_site_and_more")]

    def test_site_values_are_carried_over_to_scope(self):
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(self.migrate_from)

        old_apps = executor.loader.project_state(self.migrate_from).apps
        Site = old_apps.get_model("dcim", "Site")
        site = Site.objects.create(name="legacy-site", slug="legacy-site")
        OldCommunity = old_apps.get_model("netbox_bgp", "Community")
        OldCommunity.objects.create(value="65000:900", site=site)
        OldCommunity.objects.create(value="65000:901")

        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(self.migrate_to)

        new_apps = executor.loader.project_state(self.migrate_to).apps
        NewCommunity = new_apps.get_model("netbox_bgp", "Community")
        migrated = NewCommunity.objects.get(value="65000:900")
        untouched = NewCommunity.objects.get(value="65000:901")

        site_ct_id = ContentType.objects.get(app_label="dcim", model="site").pk
        self.assertEqual(migrated.scope_type_id, site_ct_id)
        self.assertEqual(migrated.scope_id, site.pk)
        self.assertIsNone(untouched.scope_type_id)
        self.assertIsNone(untouched.scope_id)
