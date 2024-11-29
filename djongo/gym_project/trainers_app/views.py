from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gym_app.models import *
from .models import *
from .forms import *

# Vista pel entrenador
def trainer_dashboard(request):
    return render(request, 'trainers_app/dashboard.html')

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
