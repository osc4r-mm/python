from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_user, name='delete_user'),
    path('routine/create/', views.create_routine, name='create_routine'),
    path('exercise/create', views.create_exercise, name='create_exercise'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('admin/', admin.site.urls),
    ]