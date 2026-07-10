from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'member', 'amount', 'payment_method', 'payment_status', 'payment_date']
    search_fields = ['invoice_number', 'member__member_id', 'member__user__username']
    list_filter = ['payment_method', 'payment_status', 'payment_date']

admin.site.register(Payment, PaymentAdmin)
