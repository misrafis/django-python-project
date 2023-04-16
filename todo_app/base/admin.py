from django.contrib import admin
from .models import Task

# Rejestracja modelu Task w admin panelu
admin.site.register(Task)
