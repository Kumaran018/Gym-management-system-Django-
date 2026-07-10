from django.contrib import admin
from .models import WorkoutPlan, Exercise

class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1

class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['member', 'trainer', 'start_date', 'end_date']
    search_fields = ['member__member_id', 'member__user__username', 'trainer__trainer_id']
    list_filter = ['start_date', 'end_date']
    inlines = [ExerciseInline]

admin.site.register(WorkoutPlan, WorkoutPlanAdmin)
admin.site.register(Exercise)
