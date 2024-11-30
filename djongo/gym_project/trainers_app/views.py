from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gym_app.models import *
from .models import *
from .forms import *
from gym_app.utils import role_required

# Vista del home de l'entrenador
@login_required
@role_required('trainer')
def trainer_dashboard(request):
    return render(request, 'trainers_app/dashboard.html')

# Routines
@login_required
@role_required('trainer')
def view_routines(request):
    routines = Routine.objects.all()

    for routine in routines:
        total_duration = 0
        for routine_exercise in routine.routineexercise_set.all():
            total_duration += routine_exercise.duration
        routine.total_duration = total_duration

    context = {
        'routines': routines
    }
    return render(request, 'trainers_app/routines.html', context)

@login_required
@role_required('trainer')
def view_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)
    
    routine_exercises = routine.routineexercise_set.all()
    
    total_duration = sum(r_ex.duration for r_ex in routine_exercises)
    
    context = {
        'routine': routine,
        'routine_exercises': routine_exercises,
        'total_duration': total_duration
    }
    
    return render(request, 'trainers_app/routine.html', context)

@login_required
@role_required('trainer')
def create_routine(request):
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
            return redirect('view_routines')
        else:
            messages.add_message(request, messages.ERROR, 'Error al crear la rutina.', extra_tags='danger')
    else:
        form = RoutineForm()

    exercises = Exercise.objects.all()
    if not exercises:
        messages.warning(request, 'No hay ejercicios disponibles para seleccionar.')
    
    duration_range = range(1, 61)

    context = {
        'form': form,
        'exercises': exercises,
        'duration_range': duration_range
    }
    return render(request, 'trainers_app/form_routine.html', context)

@login_required
@role_required('trainer')
def edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, f'El ejercicio {exercise.name} ha sido eliminado exitosamente.')
            return redirect('view_exercises')
        else:
            messages.add_message(request, messages.ERROR, 'No se pudo editar el ejercicio', extra_tags='danger')
    else:
        form = ExerciseForm(instance=exercise)

    context = {
        'form': form,
        'exercise': exercise,
        'edit_mode': True
    }
    return render(request, 'trainers_app/form_exercise.html', context)

@login_required
@role_required('trainer')
def delete_routine(request, routine_id):
    routine = get_object_or_404(Routine, pk=routine_id)

    if request.method == 'POST':
        routine.delete()
        messages.success(request, f'La rutina ha sido eliminado exitosamente.')
    else:
        messages.add_message(request, messages.ERROR, 'No es pot eliminar la rutina.', extra_tags='danger')
    
    return redirect('view_exercises')

# Exercises
@login_required
@role_required('trainer')
def view_exercises(request):
    exercises = Exercise.objects.all()

    context = {
        'exercises': exercises
    }
    return render(request, 'trainers_app/exercises.html', context)

@login_required
@role_required('trainer')
def view_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    
    context = {
        'exercise': exercise
    }
    return render(request, 'trainers_app/exercise.html', context)

@login_required
@role_required('trainer')
def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio creado correctamente.')
            return redirect('view_exercises')
        else:
            messages.add_message(request, messages.ERROR, 'Error al crear el ejercicio.', extra_tags='danger')
    else:
        form = ExerciseForm()
    
    context = {
        'form': form
    }
    return render(request, 'trainers_app/form_exercise.html', context)

@login_required
@role_required('trainer')
def edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, f'El ejercicio {exercise.name} ha sido eliminado exitosamente.')
            return redirect('view_exercises')
        else:
            messages.add_message(request, messages.ERROR, 'No se pudo editar el ejercicio', extra_tags='danger')
    else:
        form = ExerciseForm(instance=exercise)

    context = {
        'form': form,
        'exercise': exercise,
        'edit_mode': True
    }
    return render(request, 'trainers_app/form_exercise.html', context)

@login_required
@role_required('trainer')
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == 'POST':
        exercise.delete()
        messages.success(request, f'El ejercicio {exercise.name} ha sido eliminado exitosamente.')
    else:
        messages.add_message(request, messages.ERROR, 'No se puede eliminar el ejercicio.', extra_tags='danger')
    
    return redirect('view_exercises')
    
@login_required
def view_schedule(request):
    return render(request, 'trainers_app/schedule.html')

@login_required
def edit_schedule(request):
    return render(request, 'trainers_app/schedule.html')