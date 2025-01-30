from django.db import models
from gym_app.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserSubscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('basic', '1 rutina/semana - 15€'),
        ('medium', '3 rutines/semana - 30€'),
        ('premium', 'Il·limitades - 50€')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES)
    subscription_date = models.DateField(auto_now_add=True)
    monthly_usage = models.PositiveIntegerField(default=0)  # Contador de rutinas usadas

class WorkoutClass(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'trainers'})
    date = models.DateField()
    time = models.TimeField()
    max_participants = models.PositiveIntegerField(default=10)
    participants = models.ManyToManyField(User, through='ClassBooking', related_name='booked_classes')
    
    # Opcionales para seguimiento
    effort = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    difficulty = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

class ClassBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_class = models.ForeignKey(WorkoutClass, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)