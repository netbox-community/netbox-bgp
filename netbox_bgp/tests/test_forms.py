from http import HTTPStatus

from django.test import TestCase

from netbox_bgp.forms import ASNForm


class TestASNFormCase(TestCase):
    def test_asn_invalid_letters(self):
        form = ASNForm(
            data={
                'number': 'dsad',
                'status': 'active'
            }
        )
        self.assertEqual(
            form.errors['number'], ['Invalid AS Number: dsad']
        )

    def test_asn_asdot_valid(self):
        form = ASNForm(
            data={
                'number': '1.1',
                'status': 'active'
            }
        )
        self.assertEqual(
            form.errors.get('number'), None
        )

    def test_asn_invalid_range(self):
        form = ASNForm(
            data={
                'number': '65536.1',
                'status': 'active'
            }
        )
        self.assertEqual(
            form.errors['number'], ['Invalid AS Number: 65536.1']
        )
