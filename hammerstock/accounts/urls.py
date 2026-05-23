from django.urls import path 
from . import views

urlpatterns = [
    # Landing page-first page visitors see
    path('', views.landing, name='landing'),

    # Login and logout
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register-user/', views.register_user, name='register_user'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),
]

