from django.shortcuts import render, redirect
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

    context = {
        'form': form
    }
    return render(request, 'admin_app/register.html', context)

@login_required
@role_required('admin')
def list_users(request):
    users = User.objects.all().order_by('role', 'username')
    
    context = {
        'users': users
    }
    return render(request, 'admin_app/list_users.html', context)

@login_required
@role_required('admin')
def edit_user(request, user_id):
    try:
        user_to_edit = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect('list_users_admin')
    
    if request.method == 'POST':
        form = AdminEditUserForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f"Perfil de {user_to_edit.username} actualizado correctamente.")
            return redirect('list_users_admin')
    else:
        form = AdminEditUserForm(instance=user_to_edit)

    context = {
        'form': form, 
        'base_template': 'admin_app/base.html'
    }
    return render(request, 'admin_app/edit_user.html', context)
