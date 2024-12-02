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

    total_duration = routine.get_total_duration
    
    context = {
        'routine': routine,
        'routine_exercises': routine_exercises,
        'total_duration': total_duration,
    }
    return render(request, 'trainers_app/routine.html', context)

@login_required
@role_required('trainer')
def create_edit_routine(request, routine_id=None):
    if routine_id:
        routine = get_object_or_404(Routine, id=routine_id)
        routine_form = RoutineForm(instance=routine)
        RoutineExerciseFormSet = modelformset_factory(
            RoutineExercise,
            form=RoutineExerciseForm,
            extra=1,
            can_delete=True
        )
    else:
        routine = None
        routine_form = RoutineForm()
        RoutineExerciseFormSet = modelformset_factory(
            RoutineExercise,
            form=RoutineExerciseForm,
            extra=1
        )

    if request.method == 'POST':
        if routine_id:
            routine_form = RoutineForm(request.POST, instance=routine)
            formset = RoutineExerciseFormSet(request.POST, queryset=RoutineExercise.objects.filter(routine=routine))
        else:
            routine_form = RoutineForm(request.POST)
            formset = RoutineExerciseFormSet(request.POST, queryset=RoutineExercise.objects.none())

        if routine_form.is_valid() and formset.is_valid():
            if routine_id:
                routine_form.save()  # Guardar la rutina sin cambiar el entrenador
            else:
                routine = routine_form.save(commit=False)
                routine.trainer = request.user  # Asignar el entrenador automáticamente
                routine.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    routine_exercise = form.save(commit=False)
                    routine_exercise.routine = routine
                    routine_exercise.save()

            messages.success(request, 'Rutina guardada correctamente.')
            return redirect('view_routines')
        else:
            messages.error(request, 'Error al guardar la rutina.')

    else:
        if routine_id:
            formset = RoutineExerciseFormSet(queryset=RoutineExercise.objects.filter(routine=routine))
        else:
            formset = RoutineExerciseFormSet(queryset=RoutineExercise.objects.none())

    context = {
        'routine_form': routine_form,
        'formset': formset,
        'edit_mode': routine_id is not None,
    }
    return render(request, 'trainers_app/form_routine.html', context)

@login_required
@role_required('trainer')
def create_routine(request):
    if request.method == 'POST':
        routine_form = RoutineForm(request.POST)
        formset = RoutineExerciseFormSet(request.POST, queryset=RoutineExercise.objects.none())

        if routine_form.is_valid() and formset.is_valid():
            routine = routine_form.save(commit=False)
            routine.trainer = request.user  # Asignar el entrenador automáticamente
            routine.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    RoutineExercise.objects.create(
                        routine=routine,
                        exercise=form.cleaned_data['exercise'],
                        duration=form.cleaned_data['duration'],
                        repetitions=form.cleaned_data['repetitions']
                    )

            messages.success(request, 'Rutina creada correctamente.')
            return redirect('view_routines')
        else:
            messages.error(request, 'Error al crear la rutina.')
    else:
        routine_form = RoutineForm()
        formset = RoutineExerciseFormSet(queryset=RoutineExercise.objects.none())

    context = {
        'routine_form': routine_form,
        'formset': formset,
        'edit_mode': False,
    }
    return render(request, 'trainers_app/form_routine.html', context)

@login_required
@role_required('trainer')
def edit_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)
    RoutineExerciseFormSet = modelformset_factory(
        RoutineExercise,
        form=RoutineExerciseForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        routine_form = RoutineForm(request.POST, instance=routine)
        formset = RoutineExerciseFormSet(request.POST, queryset=RoutineExercise.objects.filter(routine=routine))

        if routine_form.is_valid() and formset.is_valid():
            routine_form.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    routine_exercise = form.save(commit=False)
                    routine_exercise.routine = routine
                    routine_exercise.save()

            messages.success(request, 'Rutina editada correctament')
            return redirect('view_routines')
        else:
            messages.add_message(request, messages.ERROR, 'Error a l\'editar la rutina.', extra_tags='danger')
    else:
        routine_form = RoutineForm(instance=routine)
        formset = RoutineExerciseFormSet(queryset=RoutineExercise.objects.filter(routine=routine))

    exercises = Exercise.objects.all()

    context = {
        'routine_form': routine_form,
        'formset': formset,
        'exercises': exercises,
        'edit_mode': True }  
    return render(request, 'trainers_app/form_routine.html', context)  

@login_required
@role_required('trainer')
def delete_routine(request, routine_id):
    routine = get_object_or_404(Routine, pk=routine_id)

    if request.method == 'POST':
        routine.delete()
        messages.success(request, f'La rutina ha sido eliminado exitosamente')
    else:
        messages.add_message(request, messages.ERROR, 'No es pot eliminar la rutina', extra_tags='danger')
    
    return redirect('view_routines')

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