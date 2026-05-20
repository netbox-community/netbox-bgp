from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from extras.models import CustomField
from ipam.models import IPAddress, ASN, RIR
from netbox.registry import registry
from netbox.search import SearchIndex

from netbox_bgp.models import (
    ASPathList,
    BGPPeerGroup,
    BGPSession,
    Community,
    CommunityList,
    PrefixList,
    RoutingPolicy,
)
from netbox_bgp.choices import (
    CommunityStatusChoices,
    IPAddressFamilyChoices,
    SessionStatusChoices,
)
from netbox_bgp.search import indexes


class SearchIndexRegistrationTestCase(TestCase):
    """Issue #257 — every plugin model should expose a SearchIndex, and each
    index should be registered with the global search registry at app-ready."""

    expected_models = {
        ASPathList,
        BGPPeerGroup,
        BGPSession,
        Community,
        CommunityList,
        PrefixList,
        RoutingPolicy,
    }

    def test_indexes_declared(self):
        self.assertEqual(
            {idx.model for idx in indexes},
            self.expected_models,
        )

    def test_indexes_subclass_searchindex(self):
        for idx in indexes:
            self.assertTrue(issubclass(idx, SearchIndex))

    def test_indexed_fields_exist_on_model(self):
        for idx in indexes:
            for field_name, _weight in idx.fields:
                idx.model._meta.get_field(field_name)

    def test_indexes_registered_in_registry(self):
        for idx in indexes:
            label = f"{idx.model._meta.app_label}.{idx.model._meta.model_name}"
            self.assertIn(label, registry["search"])
            self.assertIs(registry["search"][label], idx)


class SearchIndexToCacheTestCase(TestCase):
    """Issue #229 — SearchIndex.to_cache() must capture both declared fields
    and custom-field values so global search surfaces them."""

    @classmethod
    def setUpTestData(cls):
        rir = RIR.objects.create(name="rir_search")
        cls.local_as = ASN.objects.create(asn=65020, rir=rir)
        cls.remote_as = ASN.objects.create(asn=65021, rir=rir)
        cls.local_ip = IPAddress.objects.create(address="172.16.0.1/32")
        cls.remote_ip = IPAddress.objects.create(address="172.16.0.2/32")

    def test_to_cache_captures_declared_fields(self):
        from netbox_bgp.search import BGPSessionIndex

        session = BGPSession.objects.create(
            name="search_session",
            description="a distinctive description",
            comments="some comments",
            local_as=self.local_as,
            remote_as=self.remote_as,
            local_address=self.local_ip,
            remote_address=self.remote_ip,
            status=SessionStatusChoices.STATUS_ACTIVE,
        )

        cached = BGPSessionIndex.to_cache(session)
        cached_by_name = {ofv.name: ofv.value for ofv in cached}

        self.assertEqual(cached_by_name["name"], "search_session")
        self.assertEqual(cached_by_name["description"], "a distinctive description")
        self.assertEqual(cached_by_name["comments"], "some comments")

    def test_to_cache_captures_custom_field_values(self):
        from netbox_bgp.search import BGPSessionIndex

        cf = CustomField.objects.create(
            name="as_set",
            label="AS Set",
            type="text",
        )
        cf.object_types.set([ContentType.objects.get_for_model(BGPSession)])

        session = BGPSession.objects.create(
            name="cf_session",
            local_as=self.local_as,
            remote_as=self.remote_as,
            local_address=self.local_ip,
            remote_address=self.remote_ip,
            status=SessionStatusChoices.STATUS_ACTIVE,
            custom_field_data={"as_set": "AS-EXAMPLE"},
        )

        cached = BGPSessionIndex.to_cache(session)
        cached_by_name = {ofv.name: ofv.value for ofv in cached}

        self.assertIn("cf_as_set", cached_by_name)
        self.assertEqual(cached_by_name["cf_as_set"], "AS-EXAMPLE")

    def test_community_index_uses_value_field(self):
        from netbox_bgp.search import CommunityIndex

        community = Community.objects.create(
            value="65000:100",
            description="route-tag",
            status=CommunityStatusChoices.STATUS_ACTIVE,
        )
        cached = CommunityIndex.to_cache(community)
        names = [ofv.name for ofv in cached]
        self.assertIn("value", names)

    def test_prefix_list_index_caches_name(self):
        from netbox_bgp.search import PrefixListIndex

        pl = PrefixList.objects.create(
            name="pl_search",
            description="searchable",
            family=IPAddressFamilyChoices.FAMILY_4,
        )
        cached = PrefixListIndex.to_cache(pl)
        cached_by_name = {ofv.name: ofv.value for ofv in cached}
        self.assertEqual(cached_by_name["name"], "pl_search")
