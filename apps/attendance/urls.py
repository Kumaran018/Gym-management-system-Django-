from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.daily_attendance, name='daily_attendance'),
    path('daily/', views.daily_attendance, name='daily_attendance_alias'),
    path('history/', views.attendance_history, name='attendance_history'),
    path('reports/', views.attendance_reports, name='attendance_reports'),
]
