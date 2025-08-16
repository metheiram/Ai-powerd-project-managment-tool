def user_roles(request):
    user = request.user
    is_admin = False

    if user.is_authenticated:
        user_groups = user.groups.values_list('name', flat=True)
        is_admin = 'Admin' in user_groups

    return {
        'is_admin': is_admin
    }
