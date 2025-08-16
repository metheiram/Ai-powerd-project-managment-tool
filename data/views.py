

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
    if request.user.role in ['admin', 'manager']:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(assigned_users=request.user)
    return render(request, 'data/dashboard.html', {'projects': projects})

def settings(request):
    return render(request, 'settings.html')
