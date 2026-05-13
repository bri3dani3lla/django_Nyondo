# scheme/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Scheme Customer URLs
    path('customers/', views.customer_list, name='scheme_customer_list'),
    path('customers/add/', views.customer_add, name='scheme_customer_add'),
    path('customers/<int:pk>/', views.customer_detail, name='scheme_customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='scheme_customer_edit'),

    # Deposit URLs
    path('deposits/add/', views.deposit_add, name='deposit_add'),
    path('deposits/<int:pk>/receipt/', views.deposit_receipt, name='deposit_receipt'),
    path('deposits/<int:pk>/pickup/', views.deposit_pickup, name='deposit_pickup'),
]