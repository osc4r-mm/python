from django.shortcuts import render
from gym_app.models import *

# Vista per l'usuari
def user_dashboard(request):
    return render(request, 'users_app/dashboard.html')
