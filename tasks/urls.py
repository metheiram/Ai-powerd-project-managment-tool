from django.urls import path
from . import views
from .views import tasks_by_date

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('tab/', views.tasks_tab, name='tasks_tab'),
    path('tasks/', views.task_list, name='task_list'),
path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
path('task/<int:pk>/', views.task_detail, name='task_detail'),
  path('<int:task_id>/complete/', views.mark_task_complete, name='mark_complete'),
  path('by-date/', views.tasks_by_date, name='tasks_by_date'),
]
