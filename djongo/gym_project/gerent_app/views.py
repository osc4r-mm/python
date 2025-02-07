from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from gym_app.utils import role_required
from datetime import datetime, timedelta
from django.contrib import messages
from gym_app.models import *
from .forms import *

# Vista default per l'entrenador
@login_required
@role_required('gerent')
def gerent_dashboard(request):
    return render(request, 'gerent_app/dashboard.html')