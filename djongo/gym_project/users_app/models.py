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

class UserSubscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('basic', '1 rutina/semana - 15€'),
        ('medium', '3 rutines/semana - 30€'),
        ('premium', 'Il·limitades - 50€')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES)
    subscription_date = models.DateField(auto_now_add=True)
    
    def get_current_week_usage(self):
        # Calcula cuántas reservas ha hecho el usuario en la semana actual
        today = timezone.now().date()
        start_of_week = today - datetime.timedelta(days=today.weekday())  # Lunes
        end_of_week = start_of_week + datetime.timedelta(days=6)  # Domingo
        
        return UserCalendarRoutine.objects.filter(
            user=self.user,
            booking_date__date__range=[start_of_week, end_of_week]
        ).count()
    
    def can_book_routine(self):
        current_usage = self.get_current_week_usage()
        
        if self.plan_type == 'basic':
            return current_usage < 1
        elif self.plan_type == 'medium':
            return current_usage < 3
        elif self.plan_type == 'premium':
            return True
        return False

class UserCalendarRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar_routine = models.ForeignKey('gym_app.CalendarRoutine', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'calendar_routine')  # Un usuario no puede reservar el mismo horario 2 veces
    
    def __str__(self):
        return f"{self.user} - {self.calendar_routine}"