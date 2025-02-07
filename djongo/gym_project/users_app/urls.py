from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user'),
    path('calendar/', views.view_calendar_user, name='view_calendar_user'),
    path('join/<int:calendar_routine_id>/', views.join_routine, name='join_routine'),
    path('leave/<int:calendar_routine_id>/', views.leave_routine, name='leave_routine'),
    path('subscriptions/', views.subscription_plans, name='subscription_plans'),
    path('routines/', views.view_routines, name='routines'),
    ]