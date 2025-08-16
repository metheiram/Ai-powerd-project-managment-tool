# data/apps.py
from django.apps import AppConfig

class DataConfig(AppConfig):  # Fixed typo
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data'