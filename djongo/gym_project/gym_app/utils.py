from django.contrib import messages
from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != role:
                messages.add_message(request, messages.ERROR, 'Accés denegat', extra_tags='danger')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
