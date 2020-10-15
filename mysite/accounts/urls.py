from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views, apiviews


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name='products'),
    path('create_product/', views.createProduct, name='create_product'),
    path('customers/', views.customers, name='customers'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('update_product/<str:pk>', views.updateProduct, name='update_product'),
    path('delete_product/<str:pk>', views.deleteProduct, name='delete_product'),

    path('create_order/', views.createOrder , name="create_order"),
    path('create-order/<str:pk>/', views.createOrder1, name='create_order_pk'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    path('logout-api/', apiviews.logoutUserApi, name='logout-api'),
    path('create-user-api/', apiviews.createUserApi, name='create-user-api'),
    path('login-api/', apiviews.loginApi, name='login-api'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('customers-api/', apiviews.customersApi, name='customers-api'),
    path('create-customer-api/', apiviews.createCustomerApi,name='create-customer-api'),
    path('delete-customer-api/', apiviews.deleteCustomerApi, name='delete-customer-api'),

    path('delete-order-api/<str:pk>', apiviews.deleteOrderApi, name="delete_order-api"),
    # path('update-order-api/<str:pk>', apiviews.updateOrderApi, name="update-order-api"),

    path('hello/', apiviews.hello, name='hello'),
]