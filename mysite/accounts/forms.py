from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order, Customer, Product

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'email' ]

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Register', css_class='btn-success'))

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['customer', 'product', 'status', 'note', ]

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Register', css_class='btn-success'))

class OrderForm1(ModelForm):
	class Meta:
		model = Order
		fields = ['customer', 'product', 'status', 'note', ]

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Register', css_class='btn-success'))

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

class CostumerProfileForm(ModelForm):
	class Meta:
		model = Order
		fields = ['customer', 'product', 'status']

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Register', css_class='btn-success'))

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields ='__all__'
		
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Register', css_class='btn-success'))