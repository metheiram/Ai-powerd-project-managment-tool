

# Register your models here.
from django.contrib import admin
from .models import Project
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Project)




