from django.urls import path,include
from django.contrib import admin
from .views import generate_subtasks
from . import views
from .views import projects_by_date
app_name = 'project'

urlpatterns = [
     path('admin/', admin.site.urls),
     path('data/', include('data.urls')), 
    #path('data/', views.dashboard, name='dashboard'),
    path('project/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
     path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('register/', views.register, name='register'),
     path('project-tab/', views.project_tab, name='project_tab'),
     path('projects/create/', views.project_create, name='project_create'),
     path('generate-subtasks/', generate_subtasks, name='generate_subtasks'),
     path('generate-subtasks-api/', views.generate_subtasks_api, name='generate_subtasks_api'),

      path('by-date/', views.projects_by_date, name='projects_by_date'),
]
