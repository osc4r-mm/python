from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_user, name='delete_user'),
    path('routine/<int:routine_id>/', views.view_routine, name='view_routine'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    ]