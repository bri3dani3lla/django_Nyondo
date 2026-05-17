from django.urls import path 
from . import views

urlpatterns = [
    # Landing page-first page visitors see
    path('', views.landing, name='landing'),

    # Login and logout
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('access-denied/', views.access_denied, name='access_denied'),
]

