from .models import Project
from django.utils import timezone

def update_expired_projects():
    today = timezone.now().date()
    expired_projects = Project.objects.filter(end_date__lt=today).exclude(status__in=['completed', 'failed'])

    for project in expired_projects:
        project.status = 'failed'
        project.save()
def update_pending_projects():
    today = timezone.now().date()
    projects = Project.objects.filter(start_date__gt=today).exclude(status='pending')

    for project in projects:
        project.status = 'pending'
        project.save()
