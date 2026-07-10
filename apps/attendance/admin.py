from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['member', 'date', 'check_in_time', 'check_out_time', 'status']
    search_fields = ['member__member_id', 'member__user__username']
    list_filter = ['status', 'date']

admin.site.register(Attendance, AttendanceAdmin)
