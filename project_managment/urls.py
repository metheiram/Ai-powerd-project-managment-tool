from django.contrib import admin
from django.urls import path, include
from data.views import dashboard, index
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),  # Homepage
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard view
    path('users/', include('users.urls')),  # User module
    path('data/', include('data.urls')),  # Data module
    path('project/', include('project.urls')),  # Project module now under /project/
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('notifications/', include('notification.urls', namespace='notification')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
