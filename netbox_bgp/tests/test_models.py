from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from tenancy.models import Tenant

from netbox_bgp.models import ASN, BGPSession, Community, RoutingPolicy, BGPPeerGroup


class ASNTestCase(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='tenant')
        self.asn = ASN.objects.create(
            number=65001,
            description='test_asn'
        )

    def test_create_asn(self):
        pass

    def test_invalid_asn0(self):
        asn = ASN(number=0)
        self.assertRaises(ValidationError, asn.full_clean)

    def test_invalid_asndohuya(self):
        asn = ASN(number=4294967295)
        self.assertRaises(ValidationError, asn.full_clean)

    def test_uniqueconstraint_asn(self):
        asn = ASN(number=65001)
        with self.assertRaises(IntegrityError):
            asn.save()

    def test_uniqueconstraint_asn2(self):
        asn = ASN.objects.create(number=65001, tenant=self.tenant)
        self.assertEqual(str(asn), '65001')
        # todo cre another 65001 tenant=self.tenant
