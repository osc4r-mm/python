from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gym_app.urls')),
    path('trainer/', include('trainers_app.urls')),
    path('user/', include('users_app.urls')),
    path('gerent/', include('gerent_app.urls')),
    path('dashboard_admin/', include('admin_app.urls')),
]
