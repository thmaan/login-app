from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, CostumerProfileForm, ProductForm
from .filters import OrderFilter

# Create your views here.

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('login')
		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def customers(request):
	customers = Customer.objects.all()

	return render(request,'accounts/customers.html',{'customers':customers})

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk):
	customer = Customer.objects.get(auto_increment_id=pk)

	orders = customer.order_set.all()
	order_count = orders.count()

	context = {'customer':customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def customerProfile(request, pk):
	form = CostumerProfileForm()
	if request.method == 'POST':
		form = CostumerProfileForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form }
	return render(request,'accounts/costumer_profile.html',context)	

@login_required(login_url='login')
def createCustomer(request):
	form = CustomerForm();
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form }
	return render(request,'accounts/add_customer.html',context)

@login_required(login_url='login')
def createOrder1(request, pk):
	customer = Customer.objects.get(auto_increment_id=pk)
	form = OrderForm(instance=customer)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid:
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required
def createProduct(request):
	form = ProductForm()
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request,'accounts/add_product.html', context)

@login_required(login_url='login')
def updateCustomer(request, pk):
	customer = Customer.objects.get(auto_increment_id=pk)
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'accounts/add_customer.html', context)

@login_required(login_url='login')
def updateProduct(request, pk):
	product = Product.objects.get(id=pk)
	form = ProductForm(instance=product)
	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = { 'form': form}		
	return render(request, 'accounts/add_product.html', context) 

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete_order.html', context)

@login_required(login_url='login')
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == 'POST':
		product.delete()
		return redirect('/')
	context = {'item':product}
	return render(request, 'accounts/delete_product.html', context)