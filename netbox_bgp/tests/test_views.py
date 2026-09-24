from utilities.testing import TestCase, ViewTestCases
from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site
from ipam.models import Prefix, IPAddress, ASN, RIR
from tenancy.models import Tenant
from virtualization.models import VirtualMachine

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


# ---------------------------------------------------------------------------
# Regression tests: BGP object data must not leak past object permissions
# ---------------------------------------------------------------------------
# A ViewTab's `permission` only hides the tab link; the URL behind it is
# still directly reachable. Likewise, get_extra_context() tables were built
# straight from the database. Both must restrict to what the viewing user
# is permitted to see, independently of whether they can view the parent
# object the tab/page belongs to.

class BGPSessionTabPermissionTestCase(TestCase):
    """The BGP Sessions tab registered on core objects (template_content.py,
    plus the legacy VMBGPSessionView in views.py) must not return session
    data to a user who lacks netbox_bgp.view_bgpsession, even though they
    can view the parent object the tab is attached to.

    The Device tab (DeviceBGPSessionTabView) is registered only when the
    `device_ext_page` plugin setting is 'tab', which isn't the default test
    configuration, so it isn't exercised here.
    """

    user_permissions = ()

    @classmethod
    def setUpTestData(cls):
        cls.site = Site.objects.create(name='tabperm_site')
        cls.tenant = Tenant.objects.create(name='tabperm_tenant', slug='tabperm-tenant')
        mfr = Manufacturer.objects.create(name='tabperm_mfr')
        dt = DeviceType.objects.create(manufacturer=mfr, model='tabperm_dt')
        role = DeviceRole.objects.create(name='tabperm_role')
        cls.device = Device.objects.create(
            name='tabperm_device', site=cls.site, role=role, device_type=dt,
        )
        cls.interface = Interface.objects.create(device=cls.device, name='tabperm_eth0')
        cls.vm = VirtualMachine.objects.create(name='tabperm_vm', status='active')

        rir = RIR.objects.create(name='tabperm_rir')
        cls.local_as = ASN.objects.create(asn=65700, rir=rir)
        cls.remote_as = ASN.objects.create(asn=65701, rir=rir)

        cls.local_ip = IPAddress.objects.create(address='198.51.100.1/32')
        cls.remote_ip = IPAddress.objects.create(
            address='198.51.100.2/32', assigned_object=cls.interface,
        )
        cls.remote_prefix = Prefix.objects.create(prefix='203.0.113.0/24')

        # Linked to device, site, tenant, an interface-assigned IP, and the
        # ASNs: exercises the Site, Tenant, IPAddress, ASN and Interface tabs
        # with a single object.
        cls.session = BGPSession.objects.create(
            name='tabperm_session',
            site=cls.site,
            tenant=cls.tenant,
            device=cls.device,
            local_address=cls.local_ip,
            remote_address=cls.remote_ip,
            local_as=cls.local_as,
            remote_as=cls.remote_as,
            status='active',
        )
        # A prefix-peered session, to exercise the Prefix tab.
        cls.prefix_session = BGPSession.objects.create(
            name='tabperm_prefix_session',
            device=cls.device,
            local_address=cls.local_ip,
            remote_prefix=cls.remote_prefix,
            local_as=cls.local_as,
            remote_as=cls.remote_as,
            status='active',
        )
        # A VM-scoped session, to exercise both Virtual Machine BGP Session tabs.
        cls.vm_session = BGPSession.objects.create(
            name='tabperm_vm_session',
            virtualmachine=cls.vm,
            local_address=cls.local_ip,
            remote_address=cls.remote_ip,
            local_as=cls.local_as,
            remote_as=cls.remote_as,
            status='active',
        )

    def _assert_tab_scoped(self, url, parent_permission, session_name):
        """A user who can view the parent object, but lacks
        netbox_bgp.view_bgpsession, must not see `session_name` at `url`.
        Once granted view_bgpsession, they must see it."""
        self.add_permissions(parent_permission)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
        self.assertNotContains(response, session_name)

        self.add_permissions('netbox_bgp.view_bgpsession')
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
        self.assertContains(response, session_name)

    def test_ipaddress_tab(self):
        self._assert_tab_scoped(
            f'/ipam/ip-addresses/{self.remote_ip.pk}/bgp-sessions/',
            'ipam.view_ipaddress',
            'tabperm_session',
        )

    def test_prefix_tab(self):
        self._assert_tab_scoped(
            f'/ipam/prefixes/{self.remote_prefix.pk}/bgp-sessions/',
            'ipam.view_prefix',
            'tabperm_prefix_session',
        )

    def test_site_tab(self):
        self._assert_tab_scoped(
            f'/dcim/sites/{self.site.pk}/bgp-sessions/',
            'dcim.view_site',
            'tabperm_session',
        )

    def test_tenant_tab(self):
        self._assert_tab_scoped(
            f'/tenancy/tenants/{self.tenant.pk}/bgp-sessions/',
            'tenancy.view_tenant',
            'tabperm_session',
        )

    def test_asn_tab(self):
        self._assert_tab_scoped(
            f'/ipam/asns/{self.local_as.pk}/bgp-sessions/',
            'ipam.view_asn',
            'tabperm_session',
        )

    def test_interface_tab(self):
        self._assert_tab_scoped(
            f'/dcim/interfaces/{self.interface.pk}/bgp-sessions/',
            'dcim.view_interface',
            'tabperm_session',
        )

    def test_virtualmachine_tab(self):
        self._assert_tab_scoped(
            f'/virtualization/virtual-machines/{self.vm.pk}/bgp-sessions/',
            'virtualization.view_virtualmachine',
            'tabperm_vm_session',
        )

    def test_virtualmachine_legacy_tab(self):
        """VMBGPSessionView (views.py): a second BGP Sessions tab registered
        on Virtual Machine, at a different URL path."""
        self._assert_tab_scoped(
            f'/virtualization/virtual-machines/{self.vm.pk}/bgpsessions/',
            'virtualization.view_virtualmachine',
            'tabperm_vm_session',
        )


class BGPRelatedTablePermissionTestCase(TestCase):
    """Related-object tables built in get_extra_context() on BGP detail
    pages must not leak data the viewing user lacks permission to see, even
    though they can view the page's own object."""

    user_permissions = ()

    @classmethod
    def setUpTestData(cls):
        cls.import_policy = RoutingPolicy.objects.create(name='relperm_import_pol')
        cls.export_policy = RoutingPolicy.objects.create(name='relperm_export_pol')

        cls.peer_group = BGPPeerGroup.objects.create(name='relperm_peer_group')
        cls.peer_group.import_policies.set([cls.import_policy])
        cls.peer_group.export_policies.set([cls.export_policy])

        cls.comm_list = CommunityList.objects.create(name='relperm_comm_list')
        cls.aspath_list = ASPathList.objects.create(name='relperm_aspath_list')
        cls.prefix_list = PrefixList.objects.create(
            name='relperm_prefix_list', family=IPAddressFamilyChoices.FAMILY_4,
        )

        cls.comm_list_rule = CommunityListRule.objects.create(
            community_list=cls.comm_list, action='permit',
            community_custom='relperm_comm_rule',
        )
        cls.aspath_list_rule = ASPathListRule.objects.create(
            aspath_list=cls.aspath_list, index=10, action='permit',
            pattern='relperm_aspath_rule',
        )
        cls.prefix_list_rule = PrefixListRule.objects.create(
            prefix_list=cls.prefix_list, index=10, action='permit',
            prefix_custom='198.51.100.0/24', description='relperm_prefix_rule',
        )

        # A single RoutingPolicyRule matching all three lists, to exercise
        # the cmrules / aspathrules / plrules tables on CommunityList /
        # ASPathList / PrefixList.
        cls.rp_rule = RoutingPolicyRule.objects.create(
            routing_policy=cls.import_policy, index=10, action='permit',
            description='relperm_rp_rule',
        )
        cls.rp_rule.match_community_list.set([cls.comm_list])
        cls.rp_rule.match_aspath_list.set([cls.aspath_list])
        cls.rp_rule.match_ip_address.set([cls.prefix_list])

        rir = RIR.objects.create(name='relperm_rir')
        local_as = ASN.objects.create(asn=65710, rir=rir)
        remote_as = ASN.objects.create(asn=65711, rir=rir)
        local_ip = IPAddress.objects.create(address='198.51.100.10/32')
        remote_ip = IPAddress.objects.create(address='198.51.100.11/32')

        cls.session = BGPSession.objects.create(
            name='relperm_session',
            local_address=local_ip,
            remote_address=remote_ip,
            local_as=local_as,
            remote_as=remote_as,
            peer_group=cls.peer_group,
            prefix_list_in=cls.prefix_list,
            status='active',
        )
        cls.session.import_policies.set([cls.import_policy])
        cls.session.export_policies.set([cls.export_policy])

    def _assert_extra_context_scoped(self, url, parent_permission, extra_permissions, needle):
        """A user who can view the page's own object, but lacks permission
        on the related object type, must not see `needle` on the page. Once
        granted, they must."""
        self.add_permissions(parent_permission)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
        self.assertNotContains(response, needle)

        self.add_permissions(*extra_permissions)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
        self.assertContains(response, needle)

    def test_bgpsession_policy_tables(self):
        url = self.session.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_bgpsession', ('netbox_bgp.view_routingpolicy',),
            'relperm_import_pol',
        )

    def test_routingpolicy_related_sessions(self):
        url = self.import_policy.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_routingpolicy', ('netbox_bgp.view_bgpsession',),
            'relperm_session',
        )

    def test_routingpolicy_rules(self):
        url = self.import_policy.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_routingpolicy', ('netbox_bgp.view_routingpolicyrule',),
            'relperm_rp_rule',
        )

    def test_bgppeergroup_policy_tables(self):
        url = self.peer_group.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_bgppeergroup', ('netbox_bgp.view_routingpolicy',),
            'relperm_import_pol',
        )

    def test_bgppeergroup_related_sessions(self):
        url = self.peer_group.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_bgppeergroup', ('netbox_bgp.view_bgpsession',),
            'relperm_session',
        )

    def test_prefixlist_rules(self):
        # PrefixListRuleTable has no description column; assert on the
        # rendered prefix instead.
        url = self.prefix_list.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_prefixlist', ('netbox_bgp.view_prefixlistrule',),
            '198.51.100.0/24',
        )

    def test_prefixlist_matching_rules(self):
        url = self.prefix_list.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_prefixlist', ('netbox_bgp.view_routingpolicyrule',),
            'relperm_rp_rule',
        )

    def test_prefixlist_related_sessions(self):
        url = self.prefix_list.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_prefixlist', ('netbox_bgp.view_bgpsession',),
            'relperm_session',
        )

    def test_communitylist_rules(self):
        url = self.comm_list.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_communitylist', ('netbox_bgp.view_communitylistrule',),
            'relperm_comm_rule',
        )

    def test_communitylist_matching_rules(self):
        url = self.comm_list.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_communitylist', ('netbox_bgp.view_routingpolicyrule',),
            'relperm_rp_rule',
        )

    def test_aspathlist_rules(self):
        url = self.aspath_list.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_aspathlist', ('netbox_bgp.view_aspathlistrule',),
            'relperm_aspath_rule',
        )

    def test_aspathlist_matching_rules(self):
        url = self.aspath_list.get_absolute_url()
        self._assert_extra_context_scoped(
            url, 'netbox_bgp.view_aspathlist', ('netbox_bgp.view_routingpolicyrule',),
            'relperm_rp_rule',
        )
