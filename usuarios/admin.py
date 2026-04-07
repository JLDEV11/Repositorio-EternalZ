from django.contrib import admin
from .models import CustomUser
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """Admin para gestionar usuarios del sistema. Muestra nombre, apellido, email y estado."""
