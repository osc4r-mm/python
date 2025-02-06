from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_dashboard, name='user'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('join/<int:calendar_routine_id>/', views.join_routine, name='join_routine'),
    path('leave/<int:calendar_routine_id>/', views.leave_routine, name='leave_routine'),
    path('subscriptions/', views.subscription_plans, name='subscription_plans'),
    ]