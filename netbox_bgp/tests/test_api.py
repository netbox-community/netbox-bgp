from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


from users.models import Token

from tenancy.models import Tenant
from netbox_bgp.models import ASN, Community


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


class ASNTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.base_url_lookup = 'plugins-api:netbox_bgp-api:asn'
        self.asn1 = ASN.objects.create(number=65000, description='test_asn1')
        self.asn2 = ASN.objects.create(number=65001, description='test_asn2')
        self.tenant = Tenant.objects.create(name='tenant')

    def test_list_asn(self):
        url = reverse(f'{self.base_url_lookup}-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_asn(self):
        url = reverse(f'{self.base_url_lookup}-detail', kwargs={'pk': self.asn1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], self.asn1.number)
        self.assertEqual(response.data['description'], self.asn1.description)

    def test_create_asn(self):
        url = reverse(f'{self.base_url_lookup}-list')
        data = {'number': 65002, 'description': 'test_asn3'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

        asn = ASN.objects.get(pk=response.data['id'])
        self.assertEqual(asn.number, data['number'])
        self.assertEqual(asn.description, data['description'])

    def test_update_asn(self):
        url = reverse(f'{self.base_url_lookup}-detail', kwargs={'pk': self.asn1.pk})

        response = self.client.patch(url, {'number': 65004}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        asn = ASN.objects.get(pk=self.asn1.pk)
        self.assertEqual(asn.number, 65004)

        response = self.client.patch(url, {'number': 65005}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        asn = ASN.objects.get(pk=self.asn1.pk)
        self.assertEqual(asn.number, 65005)

    def test_delete_task(self):
        url = reverse(f'{self.base_url_lookup}-detail', kwargs={'pk': self.asn1.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ASN.DoesNotExist):
            ASN.objects.get(pk=self.asn1.pk)

    def test_uniqueconstraint_asn(self):
        url = reverse(f'{self.base_url_lookup}-list')
        data = {'number': 65001, 'description': 'test_asn3'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'number': 65001, 'description': 'test_asn3', 'tenant': self.tenant.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CommunityTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.base_url_lookup = 'plugins-api:netbox_bgp-api:community'
        self.community1 = Community.objects.create(value='65000:65000', description='test_community')

    def test_list_community(self):
        url = reverse(f'{self.base_url_lookup}-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_asn(self):
        url = reverse(f'{self.base_url_lookup}-detail', kwargs={'pk': self.community1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], self.community1.value)
        self.assertEqual(response.data['description'], self.community1.description)

    def test_create_community(self):
        url = reverse(f'{self.base_url_lookup}-list')
        data = {'value': '65001:65001', 'description': 'test_community1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Community.objects.get(pk=response.data['id']).value, '65001:65001')
        self.assertEqual(Community.objects.get(pk=response.data['id']).description, 'test_community1')

    def test_update_community(self):
        pass

    def test_delete_community(self):
        pass
