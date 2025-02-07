from django import forms
from django.contrib.auth.forms import UserCreationForm
from gym_app.models import *

# Formulari per al registre d'usuaris nous
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Email del nou usuari'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': "Nom de l'usuari"
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Nom'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Cognoms'
        })
    )
    role = forms.ChoiceField(
        choices=[('', "Selecciona el rol de l'usuari")] + list(User.ROLE_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control text-center'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Contrasenya'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Confirmar contrasenya'
        })
    )

    class Meta:
        model = User 
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.capitalize()