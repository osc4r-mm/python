from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gym_app.models import *
from .models import *
from .forms import *
from gym_app.utils import role_required

# Vista per l'usuari
@login_required
@role_required('user')
def user_dashboard(request):
    if request.user.role != "user":
        return redirect("home")
    return render(request, 'users_app/dashboard.html')
