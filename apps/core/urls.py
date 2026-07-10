from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('general/', views.general_dashboard, name='general_dashboard'),
]
