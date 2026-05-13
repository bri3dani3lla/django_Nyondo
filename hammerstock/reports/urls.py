# reports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Reports dashboard — overview of everything
    path('', views.reports_dashboard, name='reports_dashboard'),

    # Individual reports
    path('stock/', views.stock_report, name='stock_report'),
    path('sales/', views.sales_report, name='sales_report'),
    path('scheme/', views.scheme_report, name='scheme_report'),
]
