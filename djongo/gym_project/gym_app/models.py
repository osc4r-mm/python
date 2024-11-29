from django.contrib.auth.models import AbstractUser
from django.db import models

# Definim el model d'usuari personalitzat
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('director', 'Director')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    REQUIRED_FIELDS = ['role']
    
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
    dificulty = models.CharField(max_length=50, choices=[
        ('easy', 'Principiante'),
        ('normal', 'Intermedio'),
        ('hard', 'Experto'),
    ])
    exercises = models.ManyToManyField(Exercise, through='RoutineExercise')

    def __str__(self):
        return f"Rutina de {self.trainer} a las {self.start_time.strftime('%H:%M')}"


class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()  # Duración en minutos

    
    def __str__(self):
        return f"{self.exercise.name} - {self.duration} minutos"
