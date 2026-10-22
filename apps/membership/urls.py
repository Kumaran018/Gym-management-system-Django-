from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('', views.plan_list, name='plan_list_root'),
    path('plans/', views.plan_list, name='plan_list'),
    path('plans/add/', views.plan_add, name='plan_add'),
    path('plans/edit/<int:pk>/', views.plan_edit, name='plan_edit'),
    path('plans/delete/<int:pk>/', views.plan_delete, name='plan_delete'),
    path('plans/toggle/<int:pk>/', views.plan_toggle, name='plan_toggle'),
    path('my-plan/', views.member_plan_list, name='member_plan_list'),
]
