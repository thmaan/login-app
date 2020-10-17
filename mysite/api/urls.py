from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [    
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('create-user-api/', views.createUserApi, name='create-user-api'),
    path('logout-api/', views.logoutUserApi, name='logout-api'),
    path('login-api/', views.loginApi, name='login-api'),

    path('customers-api/', views.customersApi, name='customers-api'),
    path('products-api/', views.productsApi,name='products-api'),

    path('create-product-api/', views.createProductApi,name='create-product-api'),
    path('update-product-api/<str:pk>/', views.updateProductApi, name='update-product-api'),
    path('delete-product-api/<str:pk>/', views.deleteProductApi, name='delete-product-api'),

    path('create-customer-api/', views.createCustomerApi,name='create-customer-api'),
    path('delete-customer-api/<str:pk>/', views.deleteCustomerApi, name='delete-customer-api'),


    path('delete-order-api/<str:pk>/', views.deleteOrderApi, name="delete_order-api"),
    # path('update-order-api/<str:pk>', views.updateOrderApi, name="update-order-api"),

    path('hello/', views.hello, name='hello'),
]