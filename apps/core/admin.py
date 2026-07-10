from django.contrib import admin
from .models import GymItem

class GymItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'status']
    search_fields = ['name', 'category']
    list_filter = ['category', 'status']

admin.site.register(GymItem, GymItemAdmin)
