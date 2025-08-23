

# Create your views here.

from datetime import date
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, Task,   Role 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
   
def index(request):
    return render(request, 'data/index.html')

@login_required
def dashboard(request):
    from tasks.models import Task
    from django.utils import timezone
    from django.db.models import Q, Count
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Role-specific data filtering
    if request.user.role == 'admin':
        # Admin sees all system data
        projects = Project.objects.all()
        tasks = Task.objects.all()
        users = User.objects.all()
        
        # Admin-specific metrics
        total_users = users.count()
        new_users_this_week = users.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7)).count()
        admin_specific_data = {
            'total_users': total_users,
            'new_users_this_week': new_users_this_week,
            'active_users': users.filter(last_login__gte=timezone.now() - timezone.timedelta(days=30)).count(),
            'inactive_users': users.filter(last_login__lt=timezone.now() - timezone.timedelta(days=30)).count(),
        }
    elif request.user.role == 'manager':
        # Manager sees projects they created + all tasks
        projects = Project.objects.filter(Q(created_by=request.user) | Q(assigned_users=request.user))
        tasks = Task.objects.filter(project__in=projects)
        admin_specific_data = {}
    else:
        # Regular users see only their assigned work
        projects = Project.objects.filter(assigned_users=request.user)
        tasks = Task.objects.filter(Q(assignee=request.user) | Q(team_members=request.user)).distinct()
        admin_specific_data = {}
    
    # Common metrics for all roles
    active_tasks_count = tasks.filter(status__in=['not_started', 'in_progress']).count()
    completed_tasks_count = tasks.filter(status='completed').count()
    total_tasks_count = tasks.count()
    overdue_tasks_count = tasks.filter(
        due_date__lt=timezone.now(),
        status__in=['not_started', 'in_progress']
    ).count()
    
    # Calculate completion rate
    completion_rate = round((completed_tasks_count / total_tasks_count * 100), 1) if total_tasks_count > 0 else 0
    
    # Get project status counts
    project_status_counts = projects.values('status').annotate(count=Count('status'))
    
    # Get user's personal tasks for user dashboard
    if request.user.role != 'admin':
        my_tasks = tasks.filter(assignee=request.user)
        my_active_tasks = my_tasks.filter(status__in=['not_started', 'in_progress'])
        my_completed_tasks = my_tasks.filter(status='completed')
        my_overdue_tasks = my_tasks.filter(
            due_date__lt=timezone.now(),
            status__in=['not_started', 'in_progress']
        )
        
        user_specific_data = {
            'my_tasks_count': my_tasks.count(),
            'my_active_tasks_count': my_active_tasks.count(),
            'my_completed_tasks_count': my_completed_tasks.count(),
            'my_overdue_tasks_count': my_overdue_tasks.count(),
            'my_completion_rate': round((my_completed_tasks.count() / my_tasks.count() * 100), 1) if my_tasks.count() > 0 else 0,
        }
    else:
        user_specific_data = {}
    
    context = {
        'projects': projects,
        'active_tasks_count': active_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'total_tasks_count': total_tasks_count,
        'overdue_tasks_count': overdue_tasks_count,
        'completion_rate': completion_rate,
        'project_status_counts': project_status_counts,
        'is_admin': request.user.role == 'admin',
        'is_manager': request.user.role == 'manager',
        **admin_specific_data,
        **user_specific_data,
    }
    
    return render(request, 'data/dashboard.html', context)

def settings(request):
    return render(request, 'settings.html')
