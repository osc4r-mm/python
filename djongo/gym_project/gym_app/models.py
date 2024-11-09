from django.contrib.auth.models import AbstractUser
from django.db import models

# Definim el model d'usuari personalitzat
class User(AbstractUser):
    # Definició dels rols disponibles per l'usuari
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('director', 'Director')
    ]

    # Camp d'email únic per a cada usuari
    email = models.EmailField(unique=True)
    # Camp de rol, amb una longitud màxima de 10 i opcions definides en ROLE_CHOICES
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    class Meta:
        # Nom de la taula a la base de dades
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    # Camps requerits per a la creació d'usuaris
    REQUIRED_FIELDS = ['role']
    # Defineix que l'usuari farà login amb l'email en comptes del nom d'usuari estàndard
    USERNAME_FIELD = 'email'
