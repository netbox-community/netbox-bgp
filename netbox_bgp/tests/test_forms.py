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
            form.errors['number'], ['AS number is invalid.']
        )

