from django.contrib import admin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserManager(admin.ModelAdmin):
    list_display = ['username','email','is_superuser','is_active','is_staff']
