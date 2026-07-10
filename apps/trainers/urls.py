from django.urls import path
from . import views

app_name = 'trainers'

urlpatterns = [
    path('', views.trainer_list, name='list'),
    path('add/', views.trainer_add, name='add'),
    path('edit/<int:pk>/', views.trainer_edit, name='edit'),
    path('delete/<int:pk>/', views.trainer_delete, name='delete'),
    path('members/<int:pk>/', views.trainer_members, name='members'),
]
