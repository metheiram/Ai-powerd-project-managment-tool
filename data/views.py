

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
    
    if request.user.role in ['admin', 'manager']:
        projects = Project.objects.all()
        tasks = Task.objects.all()
    else:
        projects = Project.objects.filter(assigned_users=request.user)
        tasks = Task.objects.filter(Q(assignee=request.user) | Q(team_members=request.user)).distinct()
    
    # Calculate metrics
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
    
    context = {
        'projects': projects,
        'active_tasks_count': active_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'total_tasks_count': total_tasks_count,
        'overdue_tasks_count': overdue_tasks_count,
        'completion_rate': completion_rate,
        'project_status_counts': project_status_counts,
    }
    
    return render(request, 'data/dashboard.html', context)

def settings(request):
    return render(request, 'settings.html')
