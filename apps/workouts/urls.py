from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list, name='workout_list'),
    path('add/', views.workout_add, name='workout_add'),
    path('edit/<int:pk>/', views.workout_edit, name='workout_edit'),
    path('delete/<int:pk>/', views.workout_delete, name='workout_delete'),
]
