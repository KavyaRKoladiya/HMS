from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('add/', views.doctor_create, name='doctor_create'),
    path('edit/<int:pk>/', views.doctor_update, name='doctor_update'),
    path('delete/<int:pk>/', views.doctor_delete, name='doctor_delete'),
    # history view for doctors to see past patients and upload docs
    path('history/', views.doctor_history, name='doctor_history'),
    path('register/', views.doctor_register, name='doctor_register'),
]
