from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import random
from bson.decimal128 import Decimal128

def generate_random_color():
    # Generamos colores pastel suaves
    hue = random.random()  # Tono aleatorio
    saturation = random.uniform(0.3, 0.7)  # Saturación moderada
    value = random.uniform(0.8, 1.0)  # Valor alto para colores pastel
    
    # Convertimos HSV a RGB
    import colorsys
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    
    # Convertimos a hex
    hex_color = '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0] * 255),
        int(rgb[1] * 255),
        int(rgb[2] * 255)
    )
    return hex_color

# Definim el model d'usuari personalitzat
class User(AbstractUser):
    ROLE_CHOICES = [
        ('usuari', 'Usuari'),
        ('entrenador', 'Entrenador'),
        ('gerent', 'Gerent'),
        ('admin', 'Administrador'),
    ]

    PLAN_CHOICES = [
        ('free', 'Sense Pla'),
        ('basic', 'Normal'),
        ('medium', 'Avanzat'),
        ('premium', 'Premium'),
    ]

    ROUTINE_LIMITS = {
        'free': 0,
        'basic': 1,
        'medium': 3,
        'premium': float('inf')
    }

    GENDER_CHOICES = [
        ('home', 'Home'),
        ('dona', 'Dona'),
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
    plan_type = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default="free"
    )
    routines_usage = models.PositiveIntegerField(
        default=0
    )

    height = models.IntegerField(
        blank=True, 
        null=True,
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        blank=True, 
        null=True,
    )
    age = models.PositiveIntegerField(
        blank=True, 
        null=True,
    )
    gender = models.CharField(
        max_length=6, 
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True
    )

    class Meta:
        db_table = 'users'

    def can_join_routine(self):
        return self.routines_usage < self.ROUTINE_LIMITS[self.plan_type]
    
    def join(self):
        if self.can_join_routine():
            self.routines_usage += 1
            self.save()
            return True
        return False

    def leave(self):
        if self.routines_usage > 0:
            self.routines_usage -= 1
            self.save()
            return True
        return False
    
    def save(self, *args, **kwargs):
        if isinstance(self.weight, Decimal128):
            self.weight = self.weight.to_decimal()  # 🔥 Convierte Decimal128 a Decimal de Python
        super().save(*args, **kwargs)

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
        null=True,
        blank=True,
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
        limit_choices_to={'role': 'entrenador'},
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
    background_color = models.CharField(max_length=7, default=generate_random_color)

    def get_total_duration(self):
        return sum(
            exercise.duration for exercise in self.routineexercise_set.all()
        )

    def __str__(self):
        return f"{self.name} - {self.trainer.first_name} {self.trainer.last_name}"

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
    duration = models.PositiveIntegerField(   )

    def clean(self):
        if self.duration is None or self.duration <= 0:
            raise ValidationError("La duració ha de ser un valor positiu.")
    
    def __str__(self):
        return f"{self.exercise.name} - {self.repetitions or '--'} reps - {self.duration} minuts"


# Definim el model del calendari
class CalendarRoutine(models.Model):
    DAY_OF_WEEK_CHOICES = [
        (0, 'Dilluns'),
        (1, 'Dimarts'),
        (2, 'Dimecres'),
        (3, 'Dijous'),
        (4, 'Divendres'),
        (5, 'Dissabte'),
        (6, 'Diumenge'),
    ]
    
    routine = models.ForeignKey('Routine', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES)
    time = models.TimeField()
    participants = models.ManyToManyField(
        User,
        related_name='calendar_routines'
    )

    class Meta:
        unique_together = ('routine', 'day_of_week', 'time')

    def add_participant(self, user):
        if self.participants.count() >= 10:
            raise ValidationError("Ja hi ha 10 participants a aquest horari")
        if user in self.routine.participants.all():
            raise ValidationError("No pots unirte 2 vegades a un horari")
        self.participants.add(user)

    def __str__(self):
        return f"{self.routine.name} - {self.get_day_of_week_display()} {self.time}"
