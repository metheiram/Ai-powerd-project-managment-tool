from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'assigned_users': forms.SelectMultiple(attrs={'size': 6}),
        }




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']


