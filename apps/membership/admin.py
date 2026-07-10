from django.contrib import admin
from .models import MembershipPlan, Membership

class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_months', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']

class MembershipAdmin(admin.ModelAdmin):
    list_display = ['member', 'plan', 'start_date', 'end_date', 'status']
    search_fields = ['member__member_id', 'member__user__username', 'plan__name']
    list_filter = ['status', 'start_date', 'end_date']

admin.site.register(MembershipPlan, MembershipPlanAdmin)
admin.site.register(Membership, MembershipAdmin)
