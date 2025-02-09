from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
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
    
# Formulari per editar el perfil d'un usuari
class AdminEditUserForm(forms.ModelForm):
    height = forms.IntegerField(
        min_value=50,
        max_value=250,
        required=False,
        label="Altura (cm)",
        widget=forms.NumberInput(attrs={'class': 'form-control rounded-3 border-0 bg-light', 'placeholder': 'En cm (opcional)'})
    )

    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=30,
        max_value=350,
        required=False,
        label="Pes (kg)",
        widget=forms.NumberInput(attrs={'class': 'form-control rounded-3 border-0 bg-light', 'placeholder': 'En kg (opcional)', 'step': '0.1'})
    )

    gender = forms.ChoiceField(
        choices=[('', 'Selecciona un genere')] + User.GENDER_CHOICES,
        required=False,
        label="Sexe",
        widget=forms.Select(attrs={'class': 'form-select form-select rounded-3 border-0 bg-light'}),
    )

    role = forms.ChoiceField(
        choices=[('', 'Selecciona un rol')] + User.ROLE_CHOICES,
        required=True,
        label="Rol",
        widget=forms.Select(attrs={'class': 'form-select form-select rounded-3 border-0 bg-light'}),
    )

    plan_type = forms.ChoiceField(
        choices=[('', 'Selecciona un pla')] + User.PLAN_CHOICES,
        required=True,
        label="Subscripció",
        widget=forms.Select(attrs={'class': 'form-select form-select rounded-3 border-0 bg-light'}),
    )

    age = forms.IntegerField(
        min_value=0,
        max_value=150,
        required=False,
        label="Edat",
        widget=forms.NumberInput(attrs={'class': 'form-control rounded-3 border-0 bg-light', 'placeholder': 'La teva edat (opcional)'}),
    )

    password = forms.CharField(
        required=False, 
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg rounded-3 border-0 bg-light', 'placeholder': 'Escriu una nova contrasenya'}),
    )

    class Meta:
        model = User
        # El admin puede editar todo excepto routines_usage
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'plan_type', 'height', 'weight', 'gender', 'age',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-3 border-0 bg-light'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-3 border-0 bg-light'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-3 border-0 bg-light'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg rounded-3 border-0 bg-light'
            }),
        }

    def clean_first_name(self):
        """Asegura que el primer nombre se guarde con la primera letra en mayúscula."""
        first_name = self.cleaned_data.get('first_name')
        return first_name.capitalize() if first_name else first_name

    def clean_last_name(self):
        """Asegura que el apellido se guarde con la primera letra en mayúscula."""
        last_name = self.cleaned_data.get('last_name')
        return last_name.capitalize() if last_name else last_name

    def clean_password(self):
        """
        Valida la contraseña si se introduce alguna nueva.
        Se usa validate_password para aplicar las validaciones configuradas.
        """
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as e:
                raise ValidationError(e.messages)
        return password

    def save(self, commit=True):
        """
        Guarda el usuario, aplicando el cambio de contraseña si se ha proporcionado.
        """
        user = super(AdminEditUserForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
