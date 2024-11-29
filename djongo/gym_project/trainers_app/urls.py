from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/', views.trainer_dashboard, name='trainer'),
    path('routine/create/', views.create_routine, name='create_routine'),
    path('exercise/create', views.create_exercise, name='create_exercise'),
    ]