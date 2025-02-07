from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard_admin'),
    path('register/', views.register, name='register'),
]