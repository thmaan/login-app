from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated  
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.decorators import parser_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import *

from .serializers import  UserSerializer, LoginSerializer, CustomerSerializerApi, OrderSerializer, ProductSerializerApi

from accounts.models import *
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def hello(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context={'total_orders':total_orders,'delivered':delivered,
	'pending':pending}
	
	return Response(context,status=201)

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

@api_view(['POST'])
def logoutUserApi(request):
	logout(request)
	return Response(status=200)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def customersApi(request):
	customers = Customer.objects.all()
	serializer = CustomerSerializerApi(customers, many=True)
	
	return Response(serializer.data, status=201)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def productsApi(request):
	products = Product.objects.all()
	serializer = ProductSerializerApi(products, many=True)
	
	return Response(serializer.data, status=201)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def createCustomerApi(request):
	serializer = CustomerSerializerApi(data=request.data)
	if serializer.is_valid():
		serializer.save()
	else:
		return Response(status=501)

	return Response(serializer.data, status=201)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def createProductApi(request):
	serializer = ProductSerializerApi(data=request.data)
	if serializer.is_valid():
		serializer.save()
		content = {'message': 'new product OK!'}
		return Response(content, status=201)
	else:
		return Response(status=500)
	return Response(serializer.errors, status=400)

@api_view(['POST'])
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

@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def deleteCustomerApi(request, pk):
	customer = Customer.objects.get(auto_increment_id=pk)
	customer.delete()

	return Response("Customer deleted!")

@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def deleteOrderApi(request, pk):
	order = Order.objects.get(id=pk)
	order.delete()

	return Response("Order deleted!")

@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def deleteProductApi(request, pk):
	product = Product.objects.get(id=pk)
	product.delete()

	return Response("Product deleted!")

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))	
def updateProductApi(request, pk):
	product = Product.objects.get(id=pk)
	serializer = ProductSerializerApi(instance=product,data=request.data)
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def updateOrderApi(request, pk):
	order = Order.objects.get(id=pk)
	serializer = OrderSerializer(instance=order,dat=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)