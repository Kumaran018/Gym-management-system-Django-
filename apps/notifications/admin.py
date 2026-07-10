from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title']
    list_filter = ['notification_type', 'is_read', 'created_at']

admin.site.register(Notification, NotificationAdmin)
