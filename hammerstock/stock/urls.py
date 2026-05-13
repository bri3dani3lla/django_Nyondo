from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.stock_dashboard, name='stock_dashboard'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/edit/<int:pk>/', views.supplier_edit, name='supplier_edit'),

    # Stock Entry URLs
    path('entries/', views.stock_entry_list, name='stock_entry_list'),
    path('entries/add/', views.stock_entry_add, name='stock_entry_add'),

    # Delete URLs
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
    path('entries/delete/<int:pk>/', views.stock_entry_delete, name='stock_entry_delete'),
]