from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard_admin'),
    path('register/', views.register, name='register'),
    path('list-users/', views.list_users, name='list_users_admin'),
    path('list-users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('list-users/delete/<int:user_id>/', views.delete_user, name='delete_user_admin'),
]