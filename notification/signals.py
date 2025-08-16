from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from .models import Notification
from django.urls import reverse

@receiver(post_save, sender=Task)
def notify_task_assignment(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        for user in instance.assigned_to.all():
            Notification.objects.create(
                user=user,
                message=f"You have been assigned a new task: {instance.title}",
                link=reverse('tasks:task_detail', args=[instance.pk]),
                notification_type='task_assigned'
            )
