from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.admin_home, name='admin_home'),
    path('reception/', views.admin_home, name='reception_home'),
    path('trainer/', views.admin_home, name='trainer_home'),
    path('member/', views.admin_home, name='member_home'),
    path('placeholder/<str:section_name>/', views.placeholder, name='placeholder'),
    path('settings/', views.system_settings, name='system_settings'),
]
