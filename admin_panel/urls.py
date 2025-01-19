from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.user_management, name='user_management'),
    path('reports/', views.generate_report, name='generate_report'),
    path('metrics/', views.system_metrics, name='system_metrics'),
] 