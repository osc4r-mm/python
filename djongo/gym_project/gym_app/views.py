from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registre completat amb èxit!')
            return redirect('home')
        else:
            messages.error(request, 'Error en el registre. Si us plau, corregeix els errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

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
                return redirect('home')
            else:
                messages.error(request, 'Email o contrasenya incorrectes.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Guarda los cambios en el usuario actual
            messages.success(request, 'Perfil actualitzat exitosament')
            return redirect('profile')  # Redirige a la vista de perfil
    else:
        form = EditProfileForm(instance=request.user)  # Precarga el formulario con datos del usuario actual
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('home')
