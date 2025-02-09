from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gym_app.models import *
from .models import *
from .forms import *
from gym_app.utils import role_required
from django.utils import timezone
from datetime import timedelta

# Vista default per l'usuari
@login_required
@role_required('usuari')
def user_dashboard(request):
    if request.user.role != 'usuari':
        return redirect("home")
    return render(request, 'users_app/dashboard.html')

# Vista per veure el calendari
@login_required
def view_calendar_user(request):
    base_template = 'trainers_app/base.html' if request.user.role == 'entrenador' else 'users_app/base.html'

    # Obtenir dies de la setmana
    today = timezone.now()
    day_names = dict(CalendarRoutine.DAY_OF_WEEK_CHOICES)
    week_days = []
    for i in range(7):
        day = today + timedelta(days=i)
        week_days.append({
            'name': day_names[day.weekday()],
            'date': day.strftime('%d/%m'),
            'day_index': day.weekday(),
            'is_today': day.date() == today.date()
        })

    # Ggnerar caselles de 16:00 a 21:00
    time_slots = [f"{hour}:00" for hour in range(16, 22)]

    # Obtenir rutines del calendari
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
        'base_template': base_template,
    }
    
    return render(request, 'users_app/calendar.html', context)

# Vista per unirse a una rutina del calendari
@login_required
@role_required('usuari')
def join_routine(request, calendar_routine_id):
    if request.method == 'POST':
        calendar_routine = get_object_or_404(CalendarRoutine, id=calendar_routine_id)
        
        if calendar_routine.participants.count() >= 10:
            messages.add_message(request, messages.ERROR, 'Massa tard, hi han 10 valents abans que tu', extra_tags='danger')
        
        if not request.user.can_join_routine():
                messages.add_message(request, messages.ERROR, '¡Eh, tigre! El teu pla de pobre no da per mes. ¡Actualítzat! 💪', extra_tags='danger')

        if request.user.join():
            calendar_routine.participants.add(request.user)
            if not request.user.can_join_routine():
                messages.warning(request, "Has omplert totes les teves quotes")
        
    return redirect('view_calendar_user')

# Vista per sortir d'una rutina del calendari
@login_required
@role_required('usuari')
def leave_routine(request, calendar_routine_id):
    if request.method == 'POST':
        calendar_routine = get_object_or_404(CalendarRoutine, id=calendar_routine_id)
        
        if request.user in calendar_routine.participants.all():
            calendar_routine.participants.remove(request.user)
            request.user.leave()
        
    return redirect('view_calendar_user')

# Vista per escollir subscripcio
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
            
            messages.warning(request, f"¡Adeu, ambicions! Benvingut al {plan_type}. El teu dolor sera mes economic ara. 💸🏋️‍♀️")
        
        else:
            if request.user.plan_type != plan_type:
                request.user.plan_type = plan_type
                request.user.save()
                messages.success(request, "¡Nivell de patiment actualitzat! 💪")
        
        return redirect('user')
    
    context = {
        'current_plan': request.user.plan_type
    }
    return render(request, 'users_app/subscriptions.html', context)

# Vista per veure les rutines a las que esta apuntat l'usuari
@login_required
@role_required('usuari')
def view_routines(request):
    all_sessions = list(CalendarRoutine.objects.filter(participants=request.user))
    all_sessions.sort(key=lambda s: (s.day_of_week, s.time))

    context = {
        'routines': all_sessions
    }
    return render(request, 'users_app/my_routines.html', context)
