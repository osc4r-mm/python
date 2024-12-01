from django import forms
from gym_app.models import *

class RoutineForm(forms.ModelForm):
    DIFFICULTY_CHOICES = [
        ('Principiant', 'Principiant'),
        ('Intermig', 'Intermig'),
        ('Expert', 'Expert'),
    ]

    dificulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=True)

    class Meta:
        model = Routine
        fields = ['dificulty']

# Formulario intermedio para agregar la duración de cada ejercicio en la rutina
class RoutineExerciseForm(forms.ModelForm):
    class Meta:
        model = RoutineExercise
        fields = ['exercise', 'duration', 'repetitions']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'category']

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'exercici"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripció'})
    )
    category = forms.ChoiceField(
        choices=Exercise.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )