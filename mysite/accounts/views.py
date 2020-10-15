from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated  
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, CostumerProfileForm
from .filters import OrderFilter


from .serializers import CustomerSerializer, UserSerializer, LoginSerializer
# Create your views here.

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def hello(request):
	context={'message':'hi'}
	return Response(context)


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


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def createUserApi(request):
	data = JSONParser().parse(request)
	serializer = UserSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		content = {'message': 'new User OK!'}
		return Response(content, status=201)
	else:
		return Response(status=500)
	return Response(serializer.errors, status=400)

@api_view(['POST'])
def loginApi(request):
	data = JSONParser().parse(request)
	serializer = LoginSerializer(data=data)
	if serializer.is_valid():
		content = { 'message': 'Logged'}
		return Response(content, status=201)
	else:
		return Response(status=500)
	context = {}
	return render(request,'accounts/login.html', context)

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
@api_view(['POST'])
def logoutUserApi(request):
	logout(request)
	return Response(status=200)

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
def customer(request):

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

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
def createOrder1(request):
	OrderFormSet = inlineformset_factory(Customer, Order, 
		fields=('product', 'statu	s'), extra=10 )
	customer = Customer.objects.all()
	formset = OrderFormSet(queryset=Order.objects.none()
		,instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def createOrder(request):
	#OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	#customer = Customer.objects.all()
	#formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	form = OrderForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		# formset = OrderFormSet(request.POST, instance=customer)
		# if formset.is_valid():
		# 	formset.save()
		# 	return redirect('/')
		if form.is_valid:
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

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
	return render(request, 'accounts/delete.html', context)