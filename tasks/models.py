from django.db import models
from django.conf import settings
from django.utils import timezone
from project.models import Project

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks_from_tasks_app",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    team_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='task_team_members'
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    progress = models.PositiveIntegerField(default=0)
    commands = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now() and self.status != 'completed'

    def __str__(self):
        return self.title


    def auto_update_status(self):
        if self.status not in ['completed', 'overdue']:
            if self.progress == 100:
                self.status = 'completed'
            elif self.is_overdue:
                self.status = 'overdue'
            elif self.progress > 0:
                self.status = 'in_progress'
            else:
                self.status = 'not_started'
            self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="task_user_comments")
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"TaskComment by {self.user.username} on {self.project.title}"