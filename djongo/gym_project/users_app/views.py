from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gym_app.models import *
from .models import *
from .forms import *
from gym_app.utils import role_required

# Vista per l'usuari
@login_required
@role_required('user')
def user_dashboard(request):
    if request.user.role != "user":
        return redirect("home")
    return render(request, 'users_app/dashboard.html')

@login_required
def book_calendar_routine(request, calendar_routine_id):
    # Obtenir la rutina del calendari i la suscripcio de l'usuari
    calendar_routine = get_object_or_404(CalendarRoutine, id=calendar_routine_id)
    user_subscription = get_object_or_404(UserSubscription, user=request.user)

    # Verifica si ja esta apuntat
    if UserCalendarRoutine.objects.filter(
        user=request.user, 
        calendar_routine=calendar_routine
    ).exists():
        messages.error(request, "Ja estas apuntat a aquesta clase")
        return redirect('nombre_url_listado_clases')

    # Verificar si puede reservar más rutinas
    if not user_subscription.can_book_routine():
        messages.warning(request, "Has arribat al límit semanal del teu plan")
        return redirect('nombre_url_listado_clases')

    # Crear la reserva
    UserCalendarRoutine.objects.create(
        user=request.user, 
        calendar_routine=calendar_routine
        )
    messages.success(request, "Reserva realitzada amb exit")
    return redirect('nombre_url_listado_clases')