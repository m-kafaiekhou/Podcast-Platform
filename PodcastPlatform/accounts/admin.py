from django.contrib import admin
from .models import CustomUser, Notification

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'username']
    list_filter = ['is_active', 'is_staff']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    search_fields = ['message']
    list_filter = ['title']