from django import forms
from gym_app.models import *

# Formulari per afegir rutina
class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['name', 'trainer', 'difficulty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la rutina'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            }

# Formulari per afegir la duracio y/o repeticions de cada exercici en la rutina
class RoutineExerciseForm(forms.ModelForm):
    class Meta:
        model = RoutineExercise
        fields = ['exercise', 'duration', 'repetitions']
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duració en minuts'}),
            'repetitions': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Repeticions (opcional)'}),
        }
    
    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration <= 0:
            raise forms.ValidationError("La duració ha de ser un valor positiu.")
        return duration
    
    def clean_repetitions(self):
        repetitions = self.cleaned_data.get('repetitions')
        if repetitions is not None and repetitions < 0:
            raise forms.ValidationError("Les repeticions no poden ser negatives.")
        return repetitions

# Formulari per afegir l'exercici
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'exercici"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripció'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }