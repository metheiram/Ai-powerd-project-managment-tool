from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification



@login_required
def mark_as_read(request, pk):
    notification = Notification.objects.get(pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.link or 'notification')
def notification(request):
    return render(request, 'notification/notification.html')

@login_required
def mark_all_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notification:notification')


@login_required
def notification_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    notification_count = unread_notifications.count()

    return render(request, 'notification/notification.html', {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'notification_count': notification_count
    })