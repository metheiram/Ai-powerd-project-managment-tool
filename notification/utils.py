from .models import Notification

def notify_user(user, message, notif_type, link=None):
    Notification.objects.create(
        user=user,
        message=message,
        notification_type=notif_type,
        link=link
    )
