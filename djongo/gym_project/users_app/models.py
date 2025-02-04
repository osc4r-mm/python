from django.db import models
from django.utils import timezone
from datetime import datetime
from gym_app.models import *
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
    monthly_usage = models.PositiveIntegerField(default=0)

    def can_join_routine(self):
        if self.plan_type == 'basic':
            return self.monthly_usage < 1  # Máximo 1 rutina
        elif self.plan_type == 'medium':
            return self.monthly_usage < 3  # Máximo 3 rutinas
        elif self.plan_type == 'premium':
            return True  # Ilimitado
        return False

    def increment_usage(self):
        self.monthly_usage += 1
        self.save()

class UserCalendarRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar_routine = models.ForeignKey('gym_app.CalendarRoutine', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'calendar_routine')
    
    def __str__(self):
        return f"{self.user} - {self.calendar_routine}"