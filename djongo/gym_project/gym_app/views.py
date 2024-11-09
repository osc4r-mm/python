from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

# Vista per al registre d'un nou usuari
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el nou usuari a la base de dades
            login(request, user)  # Inicia sessió automàticament després del registre
            messages.success(request, 'Registre completat amb èxit!')
            return redirect('home')
        else:
            messages.error(request, 'Error en el registre. Si us plau, corregeix els errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Vista per iniciar sessió d'un usuari
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)  # Autentica l'usuari amb email i contrasenya
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciat sessió correctament!')
                return redirect('home')
            else:
                messages.error(request, 'Email o contrasenya incorrectes.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# Vista per editar el perfil de l'usuari (requereix estar autenticat)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)  # Actualitza el perfil de l'usuari actual
        if form.is_valid():
            form.save()  # Guarda els canvis en el perfil
            messages.success(request, 'Perfil actualitzat exitosament')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)  # Precàrrega el formulari amb les dades de l'usuari actual
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
        return redirect('home')
    return render(request, 'delete_user.html', {'user': user})

# Vista per a la pàgina principal (requereix estar autenticat)
@login_required
def home(request):
    return render(request, 'home.html')

# Vista per mostrar el perfil de l'usuari (requereix estar autenticat)
@login_required
def profile(request):
    return render(request, 'profile.html')

# Vista per tancar sessió
def logout_view(request):
    logout(request)  # Tanca la sessió de l'usuari
    return redirect('home')
