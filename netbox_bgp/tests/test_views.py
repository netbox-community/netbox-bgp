from utilities.testing import ViewTestCases
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import Prefix, IPAddress, ASN, RIR

from netbox_bgp.models import (
    ASPathList,
    ASPathListRule,
    BGPSession,
    CommunityListRule,
    PrefixList,
    PrefixListRule,
    RoutingPolicy,
    RoutingPolicyRule,
    Community,
    CommunityList,
    BGPPeerGroup,
)
from netbox_bgp.choices import ActionChoices, IPAddressFamilyChoices


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _plugin_url(model_name):
    """Return the _get_base_url format string for a plugin model."""
    return f'plugins:netbox_bgp:{model_name}_{{}}'


# ---------------------------------------------------------------------------
# Bulk-import-only tests (original, kept as-is)
# ---------------------------------------------------------------------------

class ASPathListRuleTestCase(ViewTestCases.BulkImportObjectsViewTestCase):
    model = ASPathListRule

    def _get_base_url(self):
        return 'plugins:{}:{}_{{}}'.format(
            self.model._meta.app_label,
            self.model._meta.model_name
        )

    @classmethod
    def setUpTestData(cls):
        aspathlists = [
            ASPathList(name='aspathlist1'),
            ASPathList(name='aspathlist2'),
        ]
        ASPathList.objects.bulk_create(aspathlists)
        aspathlistrules = [
            ASPathListRule(aspath_list=aspathlists[0],index=5,action='permit',pattern='65000')
        ]
        ASPathListRule.objects.bulk_create(aspathlistrules)
        cls.csv_data = (
            "aspath_list,index,action,pattern",
            f"{aspathlists[0].name},10,permit,65001",
            f"{aspathlists[1].name},20,permit,65002",
        )
        cls.csv_update_data = (
            "id,aspath_list,index,action,pattern",
            f"{aspathlistrules[0].pk},{aspathlists[0].name},5,deny,65000",
        )

class PrefixListRuleTestCase(ViewTestCases.BulkImportObjectsViewTestCase):
    model = PrefixListRule

    def _get_base_url(self):
        return 'plugins:{}:{}_{{}}'.format(
            self.model._meta.app_label,
            self.model._meta.model_name
        )

    @classmethod
    def setUpTestData(cls):
        prefixes = [
            Prefix(prefix='1.1.1.0/24'),
            Prefix(prefix='2.2.2.0/24')
        ]
        Prefix.objects.bulk_create(prefixes)
        prefixlists = [
            PrefixList(name='prefixlist1'),
            PrefixList(name='prefixlist2'),
        ]
        PrefixList.objects.bulk_create(prefixlists)
        prefixlistrules = [
            PrefixListRule(prefix_list=prefixlists[0], index=5, action='permit', prefix=prefixes[0])
        ]
        PrefixListRule.objects.bulk_create(prefixlistrules)
        cls.csv_data = (
            "prefix_list,index,action,prefix",
            f"{prefixlists[0].name},10,permit,{prefixes[0].prefix}",
            f"{prefixlists[1].name},10,permit,{prefixes[1].prefix}",
        )
        cls.csv_update_data = (
            "id,prefix_list,index,action",
            f"{prefixlistrules[0].pk},{prefixlists[0].name},5,deny",
        )

class RoutingPolicyRuleTestCase(ViewTestCases.BulkImportObjectsViewTestCase):
    model = RoutingPolicyRule

    def _get_base_url(self):
        return 'plugins:{}:{}_{{}}'.format(
            self.model._meta.app_label,
            self.model._meta.model_name
        )

    @classmethod
    def setUpTestData(cls):
        aspathlists = [
            ASPathList(name='aspathlist1'),
        ]
        ASPathList.objects.bulk_create(aspathlists)
        prefixlists = [
            PrefixList(name='prefixlist1'),
            PrefixList(name='prefixlist2'),
        ]
        PrefixList.objects.bulk_create(prefixlists)
        rps = [
            RoutingPolicy(name='rp1'),
            RoutingPolicy(name='rp2'),
        ]
        RoutingPolicy.objects.bulk_create(rps)
        communities = [
            Community(value='65001:1')
        ]
        Community.objects.bulk_create(communities)
        comm_lists = [
            CommunityList(name='cl1')
        ]
        CommunityList.objects.bulk_create(comm_lists)
        rp_rules = [
            RoutingPolicyRule(routing_policy=rps[0], index=10, action='permit')
        ]
        RoutingPolicyRule.objects.bulk_create(rp_rules)

        cls.csv_data = (
            "routing_policy,index,action,match_community,match_community_list,match_aspath_list,match_ip_address,match_ipv6_address",
            f"{rps[0].name},20,permit,{communities[0].value},{comm_lists[0].name},{aspathlists[0].name},{prefixlists[0].name},{prefixlists[1].name}",
            f"{rps[1].name},10,permit,{communities[0].value},{comm_lists[0].name},{aspathlists[0].name},{prefixlists[0].name},{prefixlists[1].name}",
        )
        cls.csv_update_data = (
            "id,routing_policy,index,action",
            f"{rp_rules[0].pk},{rps[0].name},10,deny",
        )


# ---------------------------------------------------------------------------
# ASPathList — full CRUD + bulk
# ---------------------------------------------------------------------------

class ASPathListViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
):
    model = ASPathList

    form_data = {
        "name": "aspathlist_create",
        "description": "",
    }

    bulk_edit_data = {"description": "bulk edited"}

    def _get_base_url(self):
        return _plugin_url('aspathlist')

    @classmethod
    def setUpTestData(cls):
        objs = [
            ASPathList(name='aspath_vt_1', description='one'),
            ASPathList(name='aspath_vt_2', description='two'),
            ASPathList(name='aspath_vt_3', description='three'),
        ]
        ASPathList.objects.bulk_create(objs)
        objs = list(ASPathList.objects.filter(name__startswith='aspath_vt_').order_by('name'))

        cls.csv_data = (
            "name,description",
            "aspath_vt_import_1,import one",
            "aspath_vt_import_2,import two",
            "aspath_vt_import_3,import three",
        )
        cls.csv_update_data = (
            "id,name,description",
            f"{objs[0].pk},aspath_vt_1,updated",
        )


# ---------------------------------------------------------------------------
# Community — full CRUD + bulk
# ---------------------------------------------------------------------------

class CommunityViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
):
    model = Community

    form_data = {
        "value": "65100:999",
        "status": "active",
    }

    bulk_edit_data = {"description": "bulk edited"}

    def _get_base_url(self):
        return _plugin_url('community')

    @classmethod
    def setUpTestData(cls):
        objs = [
            Community(value='65200:1'),
            Community(value='65200:2'),
            Community(value='65200:3'),
        ]
        Community.objects.bulk_create(objs)
        objs = list(Community.objects.filter(value__startswith='65200:').order_by('value'))

        cls.csv_data = (
            "value,status",
            "65201:1,active",
            "65201:2,active",
            "65201:3,active",
        )
        cls.csv_update_data = (
            "id,value,status",
            f"{objs[0].pk},65200:1,active",
        )


# ---------------------------------------------------------------------------
# CommunityList — full CRUD + bulk
# ---------------------------------------------------------------------------

class CommunityListViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
):
    model = CommunityList

    form_data = {
        "name": "cl_create",
        "description": "",
    }

    bulk_edit_data = {"description": "bulk edited"}

    def _get_base_url(self):
        return _plugin_url('communitylist')

    @classmethod
    def setUpTestData(cls):
        objs = [
            CommunityList(name='cl_vt_1'),
            CommunityList(name='cl_vt_2'),
            CommunityList(name='cl_vt_3'),
        ]
        CommunityList.objects.bulk_create(objs)
        objs = list(CommunityList.objects.filter(name__startswith='cl_vt_').order_by('name'))

        cls.csv_data = (
            "name,description",
            "cl_vt_import_1,",
            "cl_vt_import_2,",
            "cl_vt_import_3,",
        )
        cls.csv_update_data = (
            "id,name,description",
            f"{objs[0].pk},cl_vt_1,updated",
        )


# ---------------------------------------------------------------------------
# RoutingPolicy — full CRUD + bulk
# ---------------------------------------------------------------------------

class RoutingPolicyViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
):
    model = RoutingPolicy

    form_data = {
        "name": "rp_create",
        "description": "",
    }

    bulk_edit_data = {"description": "bulk edited"}

    def _get_base_url(self):
        return _plugin_url('routingpolicy')

    @classmethod
    def setUpTestData(cls):
        objs = [
            RoutingPolicy(name='rp_vt_1', description='one'),
            RoutingPolicy(name='rp_vt_2', description='two'),
            RoutingPolicy(name='rp_vt_3', description='three'),
        ]
        RoutingPolicy.objects.bulk_create(objs)
        objs = list(RoutingPolicy.objects.filter(name__startswith='rp_vt_').order_by('name'))

        cls.csv_data = (
            "name,description",
            "rp_vt_import_1,import one",
            "rp_vt_import_2,import two",
            "rp_vt_import_3,import three",
        )
        cls.csv_update_data = (
            "id,name,description",
            f"{objs[0].pk},rp_vt_1,updated",
        )


# ---------------------------------------------------------------------------
# BGPPeerGroup — full CRUD + bulk
# ---------------------------------------------------------------------------

class BGPPeerGroupViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
):
    model = BGPPeerGroup

    form_data = {
        "name": "pg_create",
        "description": "",
    }

    bulk_edit_data = {"description": "bulk edited"}

    def _get_base_url(self):
        return _plugin_url('bgppeergroup')

    @classmethod
    def setUpTestData(cls):
        objs = [
            BGPPeerGroup(name='pg_vt_1', description='one'),
            BGPPeerGroup(name='pg_vt_2', description='two'),
            BGPPeerGroup(name='pg_vt_3', description='three'),
        ]
        BGPPeerGroup.objects.bulk_create(objs)
        objs = list(BGPPeerGroup.objects.filter(name__startswith='pg_vt_').order_by('name'))

        cls.csv_data = (
            "name,description",
            "pg_vt_import_1,import one",
            "pg_vt_import_2,import two",
            "pg_vt_import_3,import three",
        )
        cls.csv_update_data = (
            "id,name,description",
            f"{objs[0].pk},pg_vt_1,updated",
        )


# ---------------------------------------------------------------------------
# PrefixList — full CRUD + bulk
# ---------------------------------------------------------------------------

class PrefixListViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
):
    model = PrefixList

    form_data = {
        "name": "pl_create",
        "family": "ipv4",
        "description": "",
    }

    bulk_edit_data = {"description": "bulk edited"}

    def _get_base_url(self):
        return _plugin_url('prefixlist')

    @classmethod
    def setUpTestData(cls):
        objs = [
            PrefixList(name='pl_vt_1', family=IPAddressFamilyChoices.FAMILY_4),
            PrefixList(name='pl_vt_2', family=IPAddressFamilyChoices.FAMILY_6),
            PrefixList(name='pl_vt_3', family=IPAddressFamilyChoices.FAMILY_4),
        ]
        PrefixList.objects.bulk_create(objs)
        objs = list(PrefixList.objects.filter(name__startswith='pl_vt_').order_by('name'))

        cls.csv_data = (
            "name,family",
            "pl_vt_import_1,ipv4",
            "pl_vt_import_2,ipv6",
            "pl_vt_import_3,ipv4",
        )
        cls.csv_update_data = (
            "id,name,family",
            f"{objs[0].pk},pl_vt_1,ipv6",
        )


# ---------------------------------------------------------------------------
# ASPathListRule — CRUD (BulkImport already covered by ASPathListRuleTestCase)
# ---------------------------------------------------------------------------

class ASPathListRuleCRUDViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = ASPathListRule

    def _get_base_url(self):
        return _plugin_url('aspathlistrule')

    @classmethod
    def setUpTestData(cls):
        apl = ASPathList.objects.create(name='apl_crud_parent', description='')
        rules = [
            ASPathListRule(aspath_list=apl, index=10, action='permit', pattern='65100'),
            ASPathListRule(aspath_list=apl, index=20, action='permit', pattern='65101'),
            ASPathListRule(aspath_list=apl, index=30, action='deny',   pattern='65102'),
        ]
        ASPathListRule.objects.bulk_create(rules)

        cls.form_data = {
            'aspath_list': apl.pk,
            'index': 100,
            'action': 'permit',
            'pattern': '^65001$',
        }


# ---------------------------------------------------------------------------
# CommunityListRule — CRUD (no BulkImport, no BulkEdit registered)
# ---------------------------------------------------------------------------

class CommunityListRuleViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = CommunityListRule

    def _get_base_url(self):
        return _plugin_url('communitylistrule')

    @classmethod
    def setUpTestData(cls):
        cl = CommunityList.objects.create(name='clr_vt_parent', description='')
        community = Community.objects.create(value='65500:99', status='active')
        rules = [
            CommunityListRule(community_list=cl, action='permit', community=community),
            CommunityListRule(community_list=cl, action='deny',   community=community),
        ]
        # CommunityListRule ordering is (community_list, community) with no unique_together,
        # so two rules with same community on same list is valid per DB constraints.
        # Create a second community to get 3 distinct rules.
        community2 = Community.objects.create(value='65500:100', status='active')
        CommunityListRule.objects.bulk_create(rules)
        CommunityListRule.objects.create(community_list=cl, action='permit', community=community2)

        cls.form_data = {
            'community_list': cl.pk,
            'action': 'permit',
            'community': community.pk,
        }


# ---------------------------------------------------------------------------
# RoutingPolicyRule — CRUD (BulkImport already covered by RoutingPolicyRuleTestCase)
# ---------------------------------------------------------------------------

class RoutingPolicyRuleCRUDViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = RoutingPolicyRule

    def _get_base_url(self):
        return _plugin_url('routingpolicyrule')

    @classmethod
    def setUpTestData(cls):
        rp = RoutingPolicy.objects.create(name='rpr_crud_parent', description='')
        rules = [
            RoutingPolicyRule(routing_policy=rp, index=10, action='permit'),
            RoutingPolicyRule(routing_policy=rp, index=20, action='deny'),
            RoutingPolicyRule(routing_policy=rp, index=30, action='permit'),
        ]
        RoutingPolicyRule.objects.bulk_create(rules)

        cls.form_data = {
            'routing_policy': rp.pk,
            'index': 100,
            'action': 'permit',
        }


# ---------------------------------------------------------------------------
# PrefixListRule — CRUD (BulkImport already covered by PrefixListRuleTestCase)
# ---------------------------------------------------------------------------

class PrefixListRuleCRUDViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = PrefixListRule
    # IPNetworkField stores IPNetwork objects; skip comparing the raw string in form_data
    validation_excluded_fields = ['prefix_custom']

    def _get_base_url(self):
        return _plugin_url('prefixlistrule')

    @classmethod
    def setUpTestData(cls):
        pl = PrefixList.objects.create(
            name='plr_crud_parent', family=IPAddressFamilyChoices.FAMILY_4,
        )
        rules = [
            PrefixListRule(prefix_list=pl, index=10, action='permit', prefix_custom='10.0.0.0/8'),
            PrefixListRule(prefix_list=pl, index=20, action='deny',   prefix_custom='192.168.0.0/16'),
            PrefixListRule(prefix_list=pl, index=30, action='permit', prefix_custom='172.16.0.0/12'),
        ]
        PrefixListRule.objects.bulk_create(rules)

        cls.form_data = {
            'prefix_list': pl.pk,
            'index': 100,
            'action': 'permit',
            'prefix_custom': '0.0.0.0/0',
        }


# ---------------------------------------------------------------------------
# BGPSession — Get/List/Delete/BulkDelete/BulkEdit only
# (Create uses BGPSessionAddForm; Edit uses BGPSessionForm — incompatible form_data)
# ---------------------------------------------------------------------------

class BGPSessionViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
):
    model = BGPSession
    bulk_edit_data = {'description': 'bulk edited'}

    def _get_base_url(self):
        return _plugin_url('bgpsession')

    @classmethod
    def setUpTestData(cls):
        mfr = Manufacturer.objects.create(name='bgpsess_vt_mfr')
        dt = DeviceType.objects.create(manufacturer=mfr, model='bgpsess_vt_dt')
        role = DeviceRole.objects.create(name='bgpsess_vt_role')
        site = Site.objects.create(name='bgpsess_vt_site')
        device = Device.objects.create(
            name='bgpsess_vt_device', site=site, role=role, device_type=dt,
        )
        rir = RIR.objects.create(name='bgpsess_vt_rir')
        local_as = ASN.objects.create(asn=65600, rir=rir)
        remote_as = ASN.objects.create(asn=65601, rir=rir)

        for i in range(3):
            local_ip = IPAddress.objects.create(address=f'10.20.0.{i + 1}/32')
            remote_ip = IPAddress.objects.create(address=f'10.20.1.{i + 1}/32')
            BGPSession.objects.create(
                name=f'bgpsess_vt_{i}',
                device=device,
                local_address=local_ip,
                remote_address=remote_ip,
                local_as=local_as,
                remote_as=remote_as,
                status='active',
            )
