from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('record/', views.record_payment, name='record_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('receipt/<int:pk>/', views.generate_receipt, name='generate_receipt'),
    path('revenue/', views.monthly_revenue, name='monthly_revenue'),
]
