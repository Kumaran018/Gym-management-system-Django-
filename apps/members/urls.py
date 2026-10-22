from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.member_list, name='list'),
    path('add/', views.member_add, name='add'),
    path('edit/<int:pk>/', views.member_edit, name='edit'),
    path('delete/<int:pk>/', views.member_delete, name='delete'),
    path('profile/<int:pk>/', views.member_profile, name='profile'),
    path('assign-by-metrics/', views.calculate_and_assign_plan_view, name='assign_by_metrics'),
]
