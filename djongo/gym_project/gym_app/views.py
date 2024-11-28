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
            user = form.save()  # Guarda el nou usuari a la base de dades
            login(request, user)  # Inicia sessió automàticament després del registre
            messages.success(request, 'Registre completat amb èxit!')
            return redirect('home')
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

# Vista per eliminar un usuari (requereix estar autenticat)
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

@login_required
def create_routine(request):
    if request.user.role != 'trainer':
        messages.add_message(request, messages.ERROR, 'Només els entrenadors poden crear rutines.', extra_tags='danger')
        return redirect('home')
    
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.trainer = request.user
            routine.save()

            # Guardar los ejercicios con sus duraciones
            selected_exercises = request.POST.getlist('exercises')
            for exercise_id in selected_exercises:
                duration = request.POST.get(f'duration_{exercise_id}')
                if exercise_id and duration:
                    try:
                        duration = int(duration)  # Convertir a entero
                        if duration < 60:
                            RoutineExercise.objects.create(
                            routine=routine,
                            exercise_id=exercise_id,
                            duration=int(duration)
                        )
                    except ValueError:
                        messages.add_message(request, messages.ERROR, 'Duración inválida para el ejercicio.', extra_tags='danger')
                        return redirect("create_routine")
            
            messages.success(request, 'Rutina creada correctamente.')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Error al crear la rutina.', extra_tags='danger')
    else:
        form = RoutineForm()

    exercises = Exercise.objects.all()
    if not exercises:
        messages.warning(request, 'No hay ejercicios disponibles para seleccionar.')
    
    duration_range = range(1, 61)
    return render(request, 'create_routine.html', {
        'form': form,
        'exercises': exercises,
        'duration_range': duration_range
    })

@login_required
def view_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)
    exercises = routine.exercises.all() 
    return render(request, 'view_routine.html', {'routine': routine, 'exercises': exercises})


def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio creado correctamente.')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Error al crear el ejercicio.', extra_tags='danger')
    else:
        form = ExerciseForm()

    return render(request, 'create_exercise.html', {'form': form})
