from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gym_app.utils import role_required
from django.contrib import messages
from .forms import *

# Vista default per l'admin'
@login_required
@role_required('admin')
def admin_dashboard(request):
    return render(request, 'admin_app/dashboard.html')

# Vista per al registre d'un nou usuari
@login_required
@role_required('admin')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registre completat amb èxit!')
            form = UserRegistrationForm()
    else:
        form = UserRegistrationForm()
    return render(request, 'admin_app/register.html', {'form': form})