from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

# Formulari per al registre d'usuaris nous
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User 
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']

# Formulari per a l'inici de sessió
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# Formulari per editar el perfil d'un usuari
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Nueva contrasenya")


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

    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Debe seleccionar al menos un ejercicio.'}
    )

    class Meta:
        model = Routine
        fields = ['start_time', 'exercises']

    def clean(self):
        cleaned_data = super().clean()
        exercises = cleaned_data.get('exercises')
        total_duration = 0
        if not exercises:
            raise forms.ValidationError("Debe seleccionar al menos un ejercicios.")
        for exercise in exercises:
            duration = self.data.get(f"duration_{exercise.id}")  # Obtener la duración del ejercicio en la rutina
            if duration:
                total_duration += int(duration)
        if total_duration > 60:
            raise forms.ValidationError("La duración total de los ejercicios no puede exceder los 60 minutos.")
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

class ExerciseSelectionForm(forms.Form):
    exercises = forms.ModelMultipleChoiceField(queryset=Exercise.objects.all(), widget=forms.CheckboxSelectMultiple)
    duration = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))