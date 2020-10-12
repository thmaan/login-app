from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer
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

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ['name',  ]