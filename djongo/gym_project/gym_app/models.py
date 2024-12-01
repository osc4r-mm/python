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
    CATEGORY_CHOICES = [
        ('Força', 'Força'),
        ('Resistencia', 'Resistencia'),
        ('Flexibilitat', 'Flexibilitat'),
        ('Equilibri', 'Equilibri'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

# Definim el model de la rutina
class Routine(models.Model):
    trainer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'trainer'}
    )
    dificulty = models.CharField(max_length=50)
    exercises = models.ManyToManyField(
        Exercise, 
        through='RoutineExercise'
    )

    def __str__(self):
        return f"Rutina de {self.trainer} a las {self.start_time.strftime('%H:%M')}"


class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.PositiveIntegerField(blank=True, null=True)
    duration = models.PositiveIntegerField()

    
    def __str__(self):
        return f"{self.exercise.name} - {self.repetitions} reps - {self.duration} minuts"
