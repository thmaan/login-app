from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Customer, Order, Product
from .models import Category
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
    	model = User
    	fields = ['username', 'password', ]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)	

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ['username', 'password', ]

    def validate(self, data):
        username = data.get('username', None ) 
        password = data.get('password', None )
        user = authenticate(username = username,password = password)
        if user is None:
          raise serializers.ValidationError(
                'A user with this email and password is not found.')
        else:             
            return super(LoginSerializer, self).validate(data)


class CustomerSerializerApi(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializerApi(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'status', 'note', ]
    
class DashboardSerializer(serializers.Serializer):
    total_customers = serializers.FloatField()
    total_orders = serializers.FloatField()
    delivered = serializers.FloatField() 
    pending = serializers.FloatField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'