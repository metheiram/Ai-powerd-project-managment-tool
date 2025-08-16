# in users/decorators.py
from django.core.exceptions import PermissionDenied

def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Admin").exists()

def admin_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied("You must be an admin to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped
