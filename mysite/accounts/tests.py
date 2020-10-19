from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Order, Customer, Product, Tag
from django.contrib.auth.models import User
from accounts.forms import OrderForm, CustomerForm

import json
# Create your tests here.
class TestModels(TestCase):

	def setUp(self):
		self.customer1 = Customer.objects.create(
			name='customer 1',
			email='email@example.com')
		self.tag1 = Tag.objects.create(
			name='tag 1')
		self.product1 = Product.objects.create(
			category='In door',
			name='product 1',
			price = 1000,
			description='description 1')
		self.order1 = Order.objects.create(
			status='Pending',
			customer=self.customer1,
			product=self.product1,
			note='note test')

	def test_customer_name(self):
		self.assertEqual(self.customer1.name, 'customer 1')

	def test_customer_name(self):
		self.assertNotEqual(self.customer1.email, 'custoemr1@example.com')	

	def test_tag(self):
		self.assertEqual(self.tag1.name, 'tag 1')	

	def test_order_customer(self):	
		self.assertEqual(self.order1.customer, self.customer1)

	def test_order_product(self):	
		self.assertEqual(self.product1.name, self.product1.name)

class TestViews(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('admin','admin@admin.com','admin')
		self.products_list = reverse('products')
		self.customer_list = reverse('customers')
		self.customer1 = Customer.objects.create(
			name='customer 1',
			email='email@example.com')
		self.create_order = reverse('create_order')
		self.create_order1 = reverse('create_order_pk',args=[1])
		self.customer1 = Customer.objects.create(
			name='customer 1',
			email='email@example.com')
		self.product1 = Product.objects.create(
			category='In door',
			name='product 1',
			price = 1000,
			description='description 1')
		
	def test_products_list(self):
		self.client.login(username='admin', password='admin')
		self.response = self.client.get(self.products_list)	

		self.assertEqual(self.response.status_code, 201)
		self.assertTemplateUsed(self.response, 'accounts/products.html')

	def test_customer_list(self):
		self.client.login(username='admin', password='admin')
		self.response = self.client.get(self.customer_list)	

		self.assertEqual(self.response.status_code, 200)
		self.assertTemplateUsed(self.response, 'accounts/customers.html')

	def test_order_form(self):
		customer = Customer.objects.get(pk=1).pk
		product = Product.objects.get(pk=1).pk
		mydata= {"customer":customer,"product":product,"note":"some note","status":"Pending"}
		form = OrderForm(data=mydata)

		self.assertEqual(len(form.errors), 0)
			
	def test_create_order(self):
		customer = Customer.objects.get(pk=1).pk
		product = Product.objects.get(pk=1).pk
		mydata= {"customer":customer,"product":product,"note":"some note","status":"Pending"}
		self.client.login(username='admin', password='admin')

		self.response = self.client.post(self.create_order, mydata, follow=True)

		self.assertEqual(self.response.status_code, 200)

	