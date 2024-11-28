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

# Definim el model del exercici
class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('strength', 'Fuerza'),
        ('endurance', 'Resistencia'),
        ('flexibility', 'Flexibilidad'),
        ('balance', 'Equilibrio'),
    ])

    def __str__(self):
        return self.name

# Definim el model de la rutina
class Routine(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'trainer'})
    start_time = models.TimeField()
    exercises = models.ManyToManyField(Exercise, through='RoutineExercise')

    def __str__(self):
        return f"Rutina de {self.trainer} a las {self.start_time.strftime('%H:%M')}"


class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.exercise.name} - {self.duration} minutos"
