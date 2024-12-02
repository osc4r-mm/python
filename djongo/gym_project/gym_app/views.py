from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import *
from .forms import *

# Vista per al registre d'un nou usuari
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registre completat amb èxit!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'gym_app/register.html', {'form': form})

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
                messages.success(request, 'Has iniciat sessió correctament!')
                return redirect('dashboard')
            else:
                form.add_error(None, "Credencials incorrectes.")
    else:
        form = UserLoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'gym_app/login.html', context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role == 'trainer':
        return redirect('trainer')
    if request.user.role == 'user':
        return redirect('user')

# Vista per mostrar el perfil de l'usuari (requereix estar autenticat)
@login_required
def profile(request):
    if request.user.role == 'trainer':
        base_template = 'trainers_app/base.html'
    elif request.user.role == 'user':
        base_template = 'users_app/base.html'

    context = {
        'base_template': base_template
    }
    return render(request, 'gym_app/profile.html', context)

# Vista per editar el perfil de l'usuari (requereix estar autenticat)
@login_required
def edit_profile(request):
    if request.user.role == 'trainer':
        base_template = 'trainers_app/base.html'
    elif request.user.role == 'user':
        base_template = 'users_app/base.html'

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)  # Actualitza el perfil de l'usuari actual
        if form.is_valid():
            form.save()  # Guarda els canvis en el perfil
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
    routine = get_object_or_404(Routine, id=routine_id)
    exercises = routine.exercises.all() 

    context = {
        'routine': routine, 
        'exercises': exercises
    }
    return render(request, 'gym_app/view_routine.html', context)