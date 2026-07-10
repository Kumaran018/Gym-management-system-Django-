from django.contrib import admin
from .models import Trainer

class TrainerAdmin(admin.ModelAdmin):
    list_display = ['trainer_id', 'get_full_name', 'specialization', 'salary', 'experience_years']
    search_fields = ['trainer_id', 'user__username', 'user__first_name', 'user__last_name', 'specialization']
    list_filter = ['specialization', 'experience_years']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Trainer Name'

admin.site.register(Trainer, TrainerAdmin)
