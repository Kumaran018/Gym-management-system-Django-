from django.contrib import admin
from .models import DietPlan

class DietPlanAdmin(admin.ModelAdmin):
    list_display = ['member', 'trainer', 'start_date', 'end_date', 'daily_calories']
    search_fields = ['member__member_id', 'member__user__username']
    list_filter = ['start_date', 'end_date']

admin.site.register(DietPlan, DietPlanAdmin)
