from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser


class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('current', 'Current'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects')
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='project_assigned_users'  # ✅ Unique related name
    )

    def __str__(self):
        return self.title


