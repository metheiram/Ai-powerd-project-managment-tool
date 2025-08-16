# tasks/decorators.py

from django.core.exceptions import PermissionDenied

def is_project_manager_or_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['admin', 'manager']:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper
