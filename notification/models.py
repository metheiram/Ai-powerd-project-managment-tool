from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('task_assigned', 'Task Assigned'),
        ('project_created', 'Project Created'),
        ('deadline_alert', 'Deadline Alert'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'  # ✅ Required for template access
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='project_created')
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"
