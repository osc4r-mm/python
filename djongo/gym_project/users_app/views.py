from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gym_app.models import *
from .models import *
from .forms import *
from gym_app.utils import role_required
from django.utils import timezone
from datetime import datetime, timedelta

# Vista per l'usuari
@login_required
@role_required('user')
def user_dashboard(request):
    if request.user.role != "user":
        return redirect("home")
    return render(request, 'users_app/dashboard.html')

@login_required
def calendar_view(request):
    # Obtener días de la semana
    today = timezone.now()
    week_days = []
    for i in range(7):
        day = today + timedelta(days=i)
        week_days.append({
            'name': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][day.weekday()],
            'date': day.strftime('%d/%m'),
            'day_index': day.weekday(),
            'is_today': day.date() == today.date()
        })

    # Ggnerar caselles de 16:00 a 21:00
    time_slots = [f"{hour}:00" for hour in range(16, 22)]

    # Obtener rutinas del calendario
    calendar_data = {}
    for day in range(7):
        calendar_data[day] = {}
        routines = CalendarRoutine.objects.filter(day_of_week=day)
        for routine in routines:
            hour_str = routine.time.strftime('%H:00')
            if hour_str in time_slots:
                calendar_data[day][hour_str] = routine

    context = {
        'week_days': week_days,
        'time_slots': time_slots,
        'calendar_data': calendar_data,
    }
    
    return render(request, 'users_app/calendar.html', context)

@login_required
def join_routine(request, calendar_routine_id):
    if request.method == 'POST':
        calendar_routine = get_object_or_404(CalendarRoutine, id=calendar_routine_id)
        
        # Verificaciones
        if calendar_routine.participants.count() >= 10:
            messages.error(request, "¡Tarde piaste! Ya están los 10 valientes cupos ocupados 😢")
            return redirect('calendar_view')
            
        if not request.user.can_join_routine():
            messages.error(request, 
                f"¡Eh, tigre! Tu plan de pobre no da para tanto. ¡Actualízate! 💪")
            return redirect('calendar_view')

        # Todo OK, ¡a sufrir!
        if request.user.join():  # Esto actualiza routines_usage
            calendar_routine.participants.add(request.user)
            messages.success(request, "¡Bienvenido al club del dolor! 🏋️‍♂️")
        
    return redirect('calendar_view')

@login_required
def leave_routine(request, calendar_routine_id):
    if request.method == 'POST':
        calendar_routine = get_object_or_404(CalendarRoutine, id=calendar_routine_id)
        
        if request.user in calendar_routine.participants.all():
            calendar_routine.participants.remove(request.user)
            request.user.leave()  # Esto actualiza routines_usage
            messages.success(request, "¡Has escapado con éxito! Tu dignidad... esa es otra historia 😅")
        
    return redirect('calendar_view')

@login_required
@role_required('trainer')
def assign_routine_to_calendar(request):
    if request.method == 'POST':
        day = int(request.POST.get('day'))
        hour = request.POST.get('hour')
        routine_id = request.POST.get('routine_id')
        
        if routine_id:
            time = datetime.strptime(hour, '%H:%M').time()
            routine = get_object_or_404(Routine, id=routine_id)
            
            CalendarRoutine.objects.create(
                routine=routine,
                day_of_week=day,
                time=time
            )
            
            messages.success(request, f"¡Nueva sesión de tortura programada! 😈")
            
    return redirect('calendar_view')

@login_required
def subscription_plans(request):
    if request.method == 'POST':
        plan_type = request.POST.get('plan_type')
        current_plan_order = ['free', 'basic', 'medium', 'premium']
        
        if plan_type not in current_plan_order:
            messages.error(request, "¡Eh, no tan rápid! Aquest pla no existeix 🤨")
            return render(request, 'users_app/subscriptions.html', {'current_plan': request.user.plan_type})
        
        current_index = current_plan_order.index(request.user.plan_type)
        new_index = current_plan_order.index(plan_type)
        
        # Mirem si escull un pla millor o pitjor
        if new_index < current_index:
            request.user.routines_usage = 0
            
            # Fem fora de les rutines a l'usuari
            for routine in CalendarRoutine.objects.filter(participants=request.user):
                routine.participants.remove(request.user)
            
            request.user.plan_type = plan_type
            request.user.save()
            
            messages.warning(request, f"¡Adieu, ambicions! Benvingut al {plan_type}. El teu dolor sera mes economic ara. 💸🏋️‍♀️")
        
        else:
            if request.user.plan_type != plan_type:
                request.user.plan_type = plan_type
                request.user.save()
                messages.success(request, "¡Nivel de sufrimiento actualizado! 💪")
        
        return redirect('user')
    
    # Render subscription page
    context = {
        'current_plan': request.user.plan_type
    }
    return render(request, 'users_app/subscriptions.html', context)