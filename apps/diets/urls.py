from django.urls import path
from . import views

app_name = 'diets'

urlpatterns = [
    path('', views.diet_list, name='diet_list'),
    path('add/', views.diet_add, name='diet_add'),
    path('edit/<int:pk>/', views.diet_edit, name='diet_edit'),
    path('delete/<int:pk>/', views.diet_delete, name='diet_delete'),
]
