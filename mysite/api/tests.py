import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from accounts.models import Order, Customer, Product, Tag
from django.test import TestCase

from .serializers import CustomerSerializerApi
from accounts.models import Customer

# Create your tests here.

# class RegistrationTestCase(APITestCase):

# 	def setUp(self):
# 		self.client = APIClient()
# 		self.create_user = reverse('create-user-api')

# 	def test_registration(self):
# 		data = {"username":"testcase","password":"admin"}
# 		response = self.client.post(self.create_user, data)
# 		self.assertEquals(response.status_code, 201)

class CreateCustomerTestCase(APITestCase):

	def setUp(self):
		self.create_customer = reverse('create-customer-api')
		self.product_list = reverse ('products-api')
		self.product1 = Product.objects.create(
			category='In door',
			name='product 1',
			price = 1000,
			description='description 1')
		client = APIClient()
		self.user = User.objects.create_user('admin','admin@admin.com','admin')
		self.token = Token.objects.create(user=self.user)
		self.api_authentication()
	
	def api_authentication(self):
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def test_get_products_list_authenticated(self):
		response = self.client.get(self.product_list)
		self.assertEqual(response.status_code,201)

	def test_get_products_list_un_authenticated(self):
		self.client.force_authenticate(user=None)
		response = self.client.get(self.product_list)
		self.assertEqual(response.status_code, 401)
	
	def test_customer_au(self):
		data= {"name":"admin","password":"admin"}
		response = self.client.post(self.create_customer, data, format='json')
		self.assertEqual(response.status_code, 201)
	
	def test_update_product(self):
		data = {"name":"product updated"}
		response = self.client.post(reverse('update-product-api', kwargs={'pk': 1}), data, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content),{'name':'product updated'})
	
	def test_delete_product(self):
		response = self.client.delete(reverse('delete-product-api', kwargs={'pk': 1}))
		self.assertEqual(response.status_code, 200)
