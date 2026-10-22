from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.general_dashboard, name='general_dashboard'),
    path('general/', views.general_dashboard, name='general_dashboard_alias'),
    path('reviews/', views.customer_reviews, name='customer_reviews'),
]
