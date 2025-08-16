# urls.py in your app folder
from django.urls import path
from data import views
from users.views import profile_view
app_name = 'data'
urlpatterns = [
    path('', views.index, name='index'),  # Example URL pattern
    path('dashboard/', views.dashboard, name='dashboard'), 
    
    path('settings/', views.settings, name='settings'),
    path('profile/', profile_view, name='profile'),
]
