# data/models.py
from django.db import models

from django.conf import settings
from project.models import Project

    

class Task(models.Model):
    # Fields for your Task model
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks_from_data_app")# Assuming Task belongs to Project
   

    due_date = models.DateTimeField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.title


    def __str__(self):
        return f"Feedback on {self.project}"
class Notification(models.Model):
    
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"
    
class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    

