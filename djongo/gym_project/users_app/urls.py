from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_dashboard, name='user'),
    path('classes/', views.class_schedule, name='nombre_url_listado_clases'),
    path('book/<int:calendar_routine_id>/', views.book_calendar_routine, name='book_calendar_routine'),
    ]