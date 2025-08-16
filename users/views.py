from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test
from .decorators import is_admin,admin_required 
from project.models import Project
from tasks.models import Task
from notification.models import Notification
from django.conf import settings
from .forms import (
    UserUpdateForm,
    ProfileForm,
    PreferenceForm,
    CustomUserCreationForm,
    CustomAuthenticationForm
)
from .models import Profile

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if is_admin(user):
                return redirect('users:admin_dashboard')

            profile, created = Profile.objects.get_or_create(user=user)
            bio_filled = profile.bio and profile.bio.strip()
            skills_filled = profile.skills and profile.skills.strip()
            department_filled = profile.department and profile.department.strip()

            if bio_filled and skills_filled and department_filled:
                return redirect('dashboard')
            else:
                return redirect('users:profile_setup')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Redirecting to dashboard.")
            return redirect('users:profile_setup')  # Corrected here
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_setup_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile setup completed successfully!")
            return redirect('dashboard')
        messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'users/profile_setup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def logout_view(request):
    if request.method in ['POST', 'GET']:
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect('users:login')

@login_required
def settings_view(request):
    def get_forms():
        return {
            'user_form': UserUpdateForm(request.POST or None, instance=request.user),
            'profile_form': ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile),
            'password_form': PasswordChangeForm(request.user, request.POST or None),
            'preference_form': PreferenceForm(request.POST or None, instance=request.user),
            'profile': request.user.profile
        }

    forms = get_forms()

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            if forms['user_form'].is_valid() and forms['profile_form'].is_valid():
                forms['user_form'].save()
                forms['profile_form'].save()
                messages.success(request, "Profile updated successfully.")
                return redirect('users:settings')
            messages.error(request, "Please correct the profile form errors.")
        elif 'change_password' in request.POST:
            if forms['password_form'].is_valid():
                user = forms['password_form'].save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
                return redirect('users:settings')
            messages.error(request, "Please correct the password form errors.")
        elif 'save_preferences' in request.POST:
            if forms['preference_form'].is_valid():
                forms['preference_form'].save()
                messages.success(request, "Preferences saved successfully.")
                return redirect('users:settings')
            messages.error(request, "Please correct the preferences form errors.")
        else:
            messages.error(request, "Invalid form submission.")

    return render(request, 'users/settings.html', forms)

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users:profile')
        messages.error(request, "Please correct the form errors.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    })


@admin_required
def admin_dashboard(request):
    # Example stats
    total_users       = User.objects.count()
    total_projects    = Project.objects.count()
    open_tasks        = Task.objects.filter(status__in=['not_started','in_progress']).count()
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()


    context = {
        'total_users': total_users,
        'total_projects': total_projects,
        'open_tasks': open_tasks,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'users/admin_dashboard.html', context)


