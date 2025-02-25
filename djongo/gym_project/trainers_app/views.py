from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from gym_app.utils import role_required
from datetime import datetime, timedelta
from django.contrib import messages
from gym_app.models import *
from .forms import *

# Vista default per l'entrenador
@login_required
@role_required('entrenador')
def trainer_dashboard(request):
    return render(request, 'trainers_app/dashboard.html')

# Vista per veure totes les rutines
@login_required
@role_required('entrenador')
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
    return render(request, 'gym_app/routines.html', context)

# Funcio per fer el formset sense repetir codi en crear i editar rutina
def handle_routine_form(request, routine=None):
    is_editing = routine is not None
    
    RoutineExerciseFormSet = modelformset_factory(
        RoutineExercise,
        form=RoutineExerciseForm,
        extra=1 if is_editing else 0,
        min_num=1,
        can_delete=True
    )
    
    queryset = RoutineExercise.objects.filter(routine=routine) if routine else RoutineExercise.objects.none()
    routine_form = RoutineForm(request.POST or None, instance=routine)
    formset = RoutineExerciseFormSet(request.POST or None, queryset=queryset)
        
    return routine_form, formset

# Vista per crear rutina
@login_required
@role_required('entrenador')
def create_routine(request):
    routine_form, formset = handle_routine_form(request)

    if request.method == 'POST':
        if routine_form.is_valid() and formset.is_valid():
            total_duration = sum(
                form.cleaned_data['duration']
                for form in formset
                if form.cleaned_data and 'duration' in form.cleaned_data and not form.cleaned_data.get('DELETE', False)
            )

            if total_duration > 60:
                messages.add_message(request, messages.ERROR, 'La rutina no pot durar més de 60 minuts.', extra_tags='danger')
            else:
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

# Vista per editar rutina
@login_required
@role_required('entrenador')
def edit_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)
    routine_form, formset = handle_routine_form(request, routine)

    if request.method == 'POST':
        if routine_form.is_valid() and formset.is_valid():
            total_duration = sum(
                form.cleaned_data['duration']
                for form in formset 
                if form.cleaned_data and 'duration' in form.cleaned_data and not form.cleaned_data.get('DELETE', False)
            )

            if total_duration > 60:
                messages.add_message(request, messages.ERROR, 'La rutina no pot durar més de 60 minuts.', extra_tags='danger')
            else:
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
            messages.add_message(request, messages.ERROR, 'Error a l\'editar la rutina.', extra_tags='danger')

    context = {
        'routine': routine,
        'routine_form': routine_form,
        'formset': formset,
        'edit_mode': True
    }  
    return render(request, 'trainers_app/form_routine.html', context)

# Vista per eliminar rutina
@login_required
@role_required('entrenador')
def delete_routine(request, routine_id):
    routine = get_object_or_404(Routine, pk=routine_id)

    if request.method == 'POST':
        routine.delete()
        messages.success(request, f'La rutina ha sido eliminado exitosamente')
    else:
        messages.add_message(request, messages.ERROR, 'No es pot eliminar la rutina', extra_tags='danger')
    
    return redirect('view_routines')

# Vista per veure tots els exercicis
@login_required
@role_required('entrenador')
def view_exercises(request):
    exercises = Exercise.objects.all()

    context = {
        'exercises': exercises
    }
    return render(request, 'trainers_app/exercises.html', context)

# Vista per crear un exercici
@login_required
@role_required('entrenador')
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

# Vista per editar un exercici
@login_required
@role_required('entrenador')
def edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, f'El ejercicio {exercise.name} ha sido eliminado exitosamente.')
            return redirect('view_exercises')
        else:
            messages.add_message(request, messages.ERROR, "No es pot editar l'exercici", extra_tags='danger')
    else:
        form = ExerciseForm(instance=exercise)

    context = {
        'form': form,
        'exercise': exercise,
        'edit_mode': True
    }
    return render(request, 'trainers_app/form_exercise.html', context)

# Vista per eliminar un exercici
@login_required
@role_required('entrenador')
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == 'POST':
        exercise.delete()
        messages.success(request, f'El ejercicio {exercise.name} ha sido eliminado exitosamente.')
    else:
        messages.add_message(request, messages.ERROR, "No es pot eliminar l'exercici", extra_tags='danger')
    
    return redirect('view_exercises')

# Vista per veure el calendari
@login_required
def view_calendar_trainer(request):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Lunes

    dies_catala = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"]

    week_days = [
        {
            'name': dies_catala[i],
            'date': (start_of_week + timedelta(days=i)).strftime('%Y-%m-%d'),
            'is_today': (start_of_week + timedelta(days=i)).date() == today.date(),
            'day_index': i,
        }
        for i in range(7)
    ]

    # Generar caselles de 16:00 a 21:00
    time_slots = [f"{hour}:00" for hour in range(16, 22)]

    # obtenir routines asignades al calendari
    assigned_routines = CalendarRoutine.objects.all()

    routines = Routine.objects.all()

    # ficar les rutinas al dia y hora corresponents {día: {hora: rutina}}
    calendar_data = {i: {} for i in range(7)}
    for routine in assigned_routines:
        day = routine.day_of_week
        time = routine.time.strftime('%H:%M')
        calendar_data[day][time] = routine

    context = {
        'week_days': week_days,
        'time_slots': time_slots,
        'calendar_data': calendar_data,
        'routines': routines,
    }
    return render(request, 'trainers_app/calendar.html', context)

# Vista per assignar una rutina al calendari
@login_required
@role_required('entrenador')
def assign_routine_to_calendar(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        hour = request.POST.get('hour')
        routine_id = request.POST.get('routine_id')

        existing_routine = CalendarRoutine.objects.filter(day_of_week=day, time=hour).first()
        if existing_routine:
            messages.add_message(request, messages.ERROR, "Ja n'hi ha una rutina asignada", extra_tags='danger')
        elif routine_id:
            routine = Routine.objects.get(id=routine_id)
            CalendarRoutine.objects.create(
                routine=routine,
                day_of_week=day,
                time=hour
            )

    return redirect('view_calendar_trainer')

# Vista per treure una rutina del calendari
@login_required
@role_required('entrenador')
def remove_routine_from_calendar(request, day, hour):
    try:
        # Convertir l'hora de string ("16:00") a objecte time
        from django.utils.dateparse import parse_time
        hour_time = parse_time(hour)
        
        # Buscar la rutina per día i hora
        routine = CalendarRoutine.objects.get(
            day_of_week=day,
            time=hour_time
        )
        routine.delete()
        messages.success(request, 'Rutina eliminada correctamente.')
    except CalendarRoutine.DoesNotExist:
        messages.error(request, 'No s\'ha trobat la rutina.')
    return redirect('view_calendar_trainer')