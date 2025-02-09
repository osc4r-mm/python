from django.urls import path
from . import views
from users_app.views import view_calendar_user

urlpatterns = [
    path('', views.gerent_dashboard, name='gerent'),
    path('list-users/', views.list_users, name='list_users_gerent'),
    ]