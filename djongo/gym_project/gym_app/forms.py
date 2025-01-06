from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.password_validation import validate_password
from .models import *

# Formulari per al registre d'usuaris nous
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User 
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.capitalize()
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')

        # Verifica que la contraseña tenga al menos 8 caracteres
        if len(password2) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        # Verifica que tenga al menos una letra mayúscula
        if not any(char.isupper() for char in password2):
            raise ValidationError("La contraseña debe incluir al menos una letra mayúscula.")
        
        # Verifica que tenga al menos una letra minúscula
        if not any(char.islower() for char in password2):
            raise ValidationError("La contraseña debe incluir al menos una letra minúscula.")
        
        # Verifica que tenga al menos un carácter especial
        special_characters = "!@#$%^&*(),.?\":{}|<>"
        if not any(char in special_characters for char in password2):
            raise ValidationError("La contraseña debe incluir al menos un carácter especial.")

        return password2

# Formulari per a l'inici de sessió
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# Formulari per editar el perfil d'un usuari
class EditProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label="Nueva contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.capitalize()
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as e:
                raise ValidationError(e.messages)
        return password
    
    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
