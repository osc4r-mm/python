from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gym_app.utils import role_required
from django.core.paginator import Paginator
from django.db.models import Q
from gym_app.models import User
from .forms import *

# Vista default per l'admin'
@login_required
@role_required('gerent')
def gerent_dashboard(request):
    return render(request, 'gerent_app/dashboard.html')

@login_required
@role_required('gerent')
def list_users(request):
    # Parámetres de cerca i ordenament
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('search_field', 'all')
    sort_field = request.GET.get('sort', 'username')
    sort_direction = request.GET.get('direction', 'asc')
    page_number = request.GET.get('page', 1)

    users = User.objects.all()

    if search_query:
        if search_field == 'all':
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(gender__icontains=search_query) |
                Q(role__icontains=search_query) |
                Q(plan_type__icontains=search_query)
            )
        else:
            filter_kwargs = {f"{search_field}__icontains": search_query}
            users = users.filter(**filter_kwargs)

    order_prefix = '-' if sort_direction == 'desc' else ''
    users = users.order_by(f'{order_prefix}{sort_field}')

    # Paginacio
    paginator = Paginator(users, 5)
    page_obj = paginator.get_page(page_number)

    headers = [
        {'field': 'id', 'display': 'ID'},
        {'field': 'username', 'display': 'Usuari'},
        {'field': 'first_name', 'display': 'Nom'},
        {'field': 'last_name', 'display': 'Cognom'},
        {'field': 'email', 'display': 'Email'},
        {'field': 'height', 'display': 'Altura'},
        {'field': 'weight', 'display': 'Pes'},
        {'field': 'age', 'display': 'Edat'},
        {'field': 'gender', 'display': 'Sexe'},
        {'field': 'role', 'display': 'Rol'},
        {'field': 'plan_type', 'display': 'Pla'}
    ]

    context = {
        'users': page_obj,
        'headers': headers,
        'current_sort': sort_field,
        'current_direction': sort_direction,
        'search_query': search_query,
        'search_field': search_field,
    }
    return render(request, 'gerent_app/list_users.html', context)