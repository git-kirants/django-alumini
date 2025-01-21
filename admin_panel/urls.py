from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.user_management, name='user_management'),
    path('reports/', views.generate_report, name='generate_report'),
    path('reports/<int:report_id>/view/', views.view_report, name='view_report'),
    path('reports/<int:report_id>/download/', views.download_report, name='download_report'),
    path('metrics/', views.system_metrics, name='system_metrics'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 