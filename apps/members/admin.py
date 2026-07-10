from django.contrib import admin
from .models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'get_full_name', 'gender', 'join_date', 'status']
    search_fields = ['member_id', 'user__username', 'user__first_name', 'user__last_name', 'user__email']
    list_filter = ['gender', 'status', 'join_date']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Member Name'

admin.site.register(Member, MemberAdmin)
