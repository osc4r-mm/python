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
        choices=ROUTINE_LIMITS,
        default="free"
    )
    routines_usage = models.PositiveIntegerField(
        default=0
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
    participants = models.ManyToManyField(
        User, 
        through='RoutineSubscription', 
        related_name='subscribed_routines'
    )

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
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    routine = models.ForeignKey('Routine', on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
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
