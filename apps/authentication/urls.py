from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('receptionists/', views.receptionist_list, name='receptionist_list'),
    path('receptionists/add/', views.receptionist_add, name='receptionist_add'),
    path('receptionists/edit/<int:pk>/', views.receptionist_edit, name='receptionist_edit'),
    path('receptionists/delete/<int:pk>/', views.receptionist_delete, name='receptionist_delete'),
]
