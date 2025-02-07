from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import *


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role == 'trainer':
        return redirect('trainer')
    if request.user.role == 'user':
        return redirect('user')
    if request.user.role == 'gerent':
        return redirect('gerent')
    if request.user.role == 'admin':
        return redirect('dashboard_admin')

# Vista per iniciar sessió d'un usuari
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.ERROR, "Credencials incorrectes", extra_tags='danger')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'gym_app/login.html', context)

# Vista per mostrar el perfil de l'usuari (requereix estar autenticat)
@login_required
def profile(request):
    base_template = 'trainers_app/base.html' if request.user.role == 'trainer' else 'users_app/base.html'
    
    # Próximes rutines
    upcoming_sessions = []
    if request.user.role == 'user':
        today = timezone.now()
        current_time = today.time()
        current_weekday = today.weekday()
        
        current_week_sessions = []
        next_week_sessions = []
        today_past_sessions = []

        all_sessions = CalendarRoutine.objects.filter(participants=request.user)

        for session in all_sessions:
            if session.day_of_week == current_weekday and session.time < current_time:
                today_past_sessions.append(session)  # Les sessions d'avui que ja han passat
            elif session.day_of_week >= current_weekday:
                current_week_sessions.append(session)  # D'avui en endevant (diumenge)'
            else:
                next_week_sessions.append(session)  # Des de dilluns fins al dia actual

        # Ordenar per dia i hora
        current_week_sessions.sort(key=lambda s: (s.day_of_week, s.time))
        next_week_sessions.sort(key=lambda s: (s.day_of_week, s.time))
        today_past_sessions.sort(key=lambda s: s.time)

        upcoming_sessions = current_week_sessions + next_week_sessions + today_past_sessions

        # Nomes mostrem les 3 mes properes
        upcoming_sessions = upcoming_sessions[:3]

    context = {
        'base_template': base_template,
        'upcoming_sessions': upcoming_sessions,
        'user': request.user,
    }
    return render(request, 'gym_app/profile.html', context)

# Vista per editar el perfil de l'usuari (requereix estar autenticat)
@login_required
def edit_profile(request):
    base_template = 'trainers_app/base.html' if request.user.role == 'trainer' else 'users_app/base.html'

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualitzat exitosament')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)  # Precàrrega el formulari amb les dades de l'usuari actual

    context = {
        'form': form,
        'base_template': base_template,
    }
    return render(request, 'gym_app/edit_profile.html', context)

# Vista per eliminar un usuari (requereix estar autenticat)
@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
        return redirect('home')
    
    context = {
        'user': user
    }
    return render(request, 'gym_app/delete_user.html', context)

# Vista per tancar sessió
def logout_view(request):
    logout(request)  # Tanca la sessió de l'usuari
    return redirect('dashboard')

@login_required
def view_routine(request, routine_id):
    base_template = 'trainers_app/base.html' if request.user.role == 'trainer' else 'users_app/base.html'
    
    routine = get_object_or_404(Routine, id=routine_id)
    routine_exercises = routine.routineexercise_set.all()
    total_duration = routine.get_total_duration
    
    context = {
        'routine': routine,
        'routine_exercises': routine_exercises,
        'total_duration': total_duration,
        'base_template': base_template
    }
    return render(request, 'gym_app/routine.html', context)