from django.urls import path
from . import views
from users_app.views import view_calendar_user

urlpatterns = [
    path('', views.trainer_dashboard, name='trainer'),
    path('routines/', views.view_routines, name='view_routines'),
    path('routine/<int:routine_id>/delete/', views.delete_routine, name='delete_routine'),
    path('routine/<int:routine_id>/edit/', views.edit_routine, name='edit_routine'),
    path('routine/create/', views.create_routine, name='create_routine'),
    path('exercises/', views.view_exercises, name='view_exercises'),
    path('exercise/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),
    path('exercise/<int:exercise_id>/edit/', views.edit_exercise, name='edit_exercise'),
    path('exercise/create/', views.create_exercise, name='create_exercise'),
    path('calendar/v1', views.view_calendar_trainer, name='view_calendar_trainer'),
    path('calendar/v2', view_calendar_user, name='view_calendar'),
    path('calendar/assign/', views.assign_routine_to_calendar, name='assign_routine_to_calendar'),
    path('calendar/remove/<int:day>/<str:hour>/', views.remove_routine_from_calendar, name='remove_routine_from_calendar'),
    ]