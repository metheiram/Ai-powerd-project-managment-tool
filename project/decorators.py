from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def is_project_manager_or_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['admin', 'manager']:
            return view_func(request, *args, **kwargs)
        messages.error(request, "You are not authorized to access this page.")
        return redirect('dashboard')  # or wherever you want
    return wrapper