from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.trainer_dashboard, name='trainer'),
    path('routines/', views.view_routines, name='view_routines'),
    path('routine/<int:routine_id>/delete/', views.delete_routine, name='delete_routine'),
    path('routine/<int:routine_id>/edit/', views.edit_routine, name='edit_routine'),
    path('routine/<int:routine_id>/', views.view_routine, name='view_routine'),
    path('routine/create/', views.create_edit_routine, name='create_routine'),
    path('exercises/', views.view_exercises, name='view_exercises'),
    path('exercise/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),
    path('exercise/<int:exercise_id>/edit/', views.edit_exercise, name='edit_exercise'),
    path('exercise/<int:exercise_id>/', views.view_exercise, name='view_exercise'),
    path('exercise/create/', views.create_exercise, name='create_exercise'),
    path('schedule/', views.view_schedule, name='view_schedule'),
    path('schedule/edit/', views.edit_schedule, name='edit_schedule'),
    ]