from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

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
