from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.admin_home, name='admin_home'),
    path('reception/', views.reception_home, name='reception_home'),
    path('trainer/', views.trainer_home, name='trainer_home'),
    path('member/', views.member_home, name='member_home'),
    path('placeholder/<str:section_name>/', views.placeholder, name='placeholder'),
    path('settings/', views.system_settings, name='system_settings'),
]
