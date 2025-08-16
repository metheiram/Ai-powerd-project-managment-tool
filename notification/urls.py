from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    
    path('read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('notification/', views.notification_view, name='notification'),
    path('mark-all/', views.mark_all_as_read, name='mark_all_as_read'),

]
