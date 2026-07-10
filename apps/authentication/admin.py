from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'phone', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Attributes', {'fields': ('role', 'phone', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Attributes', {'fields': ('role', 'phone', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
