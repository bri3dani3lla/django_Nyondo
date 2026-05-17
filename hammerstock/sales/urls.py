from django.urls import path
from . import views

urlpatterns = [
    # Customer URLs
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),

    # Sale URLs
    path('', views.sale_list, name='sale_list'),
    path('add/', views.sale_add, name='sale_add'),
    path('<int:pk>/receipt/', views.sale_receipt, name='sale_receipt'),
    path('<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('dashboard/', views.sales_dashboard, name='sales_dashboard'),
]