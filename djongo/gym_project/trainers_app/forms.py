from django import forms
from gym_app.models import *

class RoutineForm(forms.ModelForm):
    TIME_CHOICES = [
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
    ]
    start_time = forms.ChoiceField(choices=TIME_CHOICES, required=True)

    class Meta:
        model = Routine
        fields = ['start_time']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

# Formulario intermedio para agregar la duración de cada ejercicio en la rutina
class RoutineExerciseForm(forms.ModelForm):
    class Meta:
        model = RoutineExercise
        fields = ['exercise', 'duration']

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