from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_customer/', views.createCustomer, name="create_customer"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('create-user-api/', views.createUserApi, name='create-user-api'),
    path('login-api/', views.loginApi, name='login-api'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('hello/', views.HelloView.as_view(), name='hello'),
]