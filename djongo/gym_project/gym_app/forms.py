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
    height = forms.IntegerField(
        min_value=50,
        max_value=250,
        required=False,
        label="Altura (cm)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control rounded-3 border-0 bg-light', 'placeholder': 'En cm (opcional)'})
    )

    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=30,
        max_value=350,
        required=False,
        label="Peso (kg)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control rounded-3 border-0 bg-light', 'placeholder': 'En kg (opcional)', 'step': '0.1'})
    )

    gender = forms.ChoiceField(
        choices=[('', 'Selecciona un genere')] + User.GENDER_CHOICES,
        required=False,
        label="Sexe",
        widget=forms.Select(attrs={'class': 'class:form-select form-select rounded-3 border-0 bg-light'}),
    )

    age = forms.IntegerField(
        min_value=0,
        max_value=150,
        required=False,
        label="Edat",
        widget=forms.NumberInput(attrs={'class': 'class:form-control form-control rounded-3 border-0 bg-light', 'placeholder': 'La teva edat (opcional)'}),
    )

    password = forms.CharField(
        required=False, 
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg rounded-3 border-0 bg-light', 'placeholder': 'Escriu una nova contrasenya'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'weight', 'height', 'gender', 'age']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg rounded-3 border-0 bg-light'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg rounded-3 border-0 bg-light'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg rounded-3 border-0 bg-light'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg rounded-3 border-0 bg-light'}),
        }
    
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
