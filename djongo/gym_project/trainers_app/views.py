from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from datetime import datetime, timedelta
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


def handle_routine_form(request, routine=None):
    is_editing = routine is not None
    
    RoutineExerciseFormSet = modelformset_factory(
        RoutineExercise,
        form=RoutineExerciseForm,
        extra=0 if is_editing else 1,
        min_num=1,
        can_delete=True
    )
    
    queryset = RoutineExercise.objects.filter(routine=routine) if routine else RoutineExercise.objects.none()
    routine_form = RoutineForm(request.POST or None, instance=routine)
    formset = RoutineExerciseFormSet(request.POST or None, queryset=queryset)
        
    return routine_form, formset

@login_required
@role_required('trainer')
def create_routine(request):
    routine_form, formset = handle_routine_form(request)

    if request.method == 'POST':
        if routine_form.is_valid() and formset.is_valid():
            routine = routine_form.save(commit=False)
            routine.trainer = request.user
            routine.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    routine_exercise = form.save(commit=False)
                    routine_exercise.routine = routine
                    routine_exercise.save()

                messages.success(request, 'Rutina creada correctament.')
                return redirect('view_routines')
        else:
            messages.add_message(request, messages.ERROR, 'Error al crear la rutina.', extra_tags='danger')

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
    routine_form, formset = handle_routine_form(request, routine)

    if request.method == 'POST':
        if routine_form.is_valid() and formset.is_valid():

            total_duration = sum(
            form.cleaned_data.get('duration', 0) 
            for form in formset 
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        )

            if total_duration < 60:
                routine_form.save()

                for form in formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                    elif form.cleaned_data:
                        routine_exercise = form.save(commit=False)
                        routine_exercise.routine = routine
                        routine_exercise.save()

                messages.success(request, 'Rutina editada correctament')
                return redirect('view_routines')
            else:
                messages.add_message(request, messages.ERROR, 'La rutina no pot durar mes de 60 minuts.', extra_tags='danger')
        else:
            messages.add_message(request, messages.ERROR, 'Error a l\'editar la rutina.', extra_tags='danger')

    context = {
        'routine': routine,
        'routine_form': routine_form,
        'formset': formset,
        'edit_mode': True
    }  
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
    # Obtener la fecha actual
    today = datetime.now()

    # Generar los días de la semana
    start_of_week = today - timedelta(days=today.weekday())  # Lunes
    week_days = [
        {
            'name': (start_of_week + timedelta(days=i)).strftime('%A'),  # Nombre del día
            'date': (start_of_week + timedelta(days=i)).strftime('%d/%m/%Y'),  # Fecha del día
            'is_today': (start_of_week + timedelta(days=i)).date() == today.date()  # Marcar si es hoy
        }
        for i in range(7)
    ]

    # Generar los horarios de 16:00 a 21:00
    time_slots = [f"{hour}:00 - {hour + 1}:00" for hour in range(16, 21)]

    context = {
        'week_days': week_days,
        'time_slots': time_slots,
    }
    return render(request, 'trainers_app/schedule.html', context)

@login_required
def edit_schedule(request):
    return render(request, 'trainers_app/schedule.html')