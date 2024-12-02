from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# Definim el model d'usuari personalitzat
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('director', 'Director'),
    ]

    email = models.EmailField(
        unique=True,
        max_length=50,
    )
    username = models.CharField(
        max_length=30,
    )
    first_name = models.CharField(
        max_length=30,
    )
    last_name = models.CharField(
        max_length=30,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES, 
        default='user',
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
    
    USERNAME_FIELD = 'email'

# Definim el model del exercici
class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('Força', 'Força'),
        ('Resistencia', 'Resistencia'),
        ('Flexibilitat', 'Flexibilitat'),
        ('Equilibri', 'Equilibri'),
    ]

    name = models.CharField(
        max_length=30,
        unique=True,
    )
    description = models.TextField(
        max_length=255,
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='Força',
    )

    def __str__(self):
        return self.name

# Definim el model de la rutina
class Routine(models.Model):
    DIFFICULTY_CHOICES = [
        ('Principiant', 'Principiant'),
        ('Intermig', 'Intermig'),
        ('Expert', 'Expert'),
    ]

    trainer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'trainer'},
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=30,
        unique=True,
    )
    difficulty = models.CharField(
        max_length=50,
        choices=DIFFICULTY_CHOICES,
    )
    exercises = models.ManyToManyField(
        Exercise, 
        through='RoutineExercise',
    )

    def get_total_duration(self):
        return sum(
            exercise.duration for exercise in self.routineexercise_set.all()
        )

    def __str__(self):
        return f"Rutina de {self.trainer} a las {self.start_time.strftime('%H:%M')}"


class RoutineExercise(models.Model):
    routine = models.ForeignKey(
        Routine, 
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        Exercise, 
        on_delete=models.CASCADE,
    )
    repetitions = models.PositiveIntegerField(
        blank=True, 
        null=True,
    )
    duration = models.PositiveIntegerField(
        blank=False, 
        null=False,
    )

    def clean(self):
        if self.duration is None or self.duration <= 0:
            raise ValidationError("La duración debe ser un valor positivo.")
    
    def __str__(self):
        return f"{self.exercise.name} - {self.repetitions or '--'} reps - {self.duration} minutos"
