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
    path('success-stories/', views.success_stories, name='success_stories'),
    path('success-stories/<int:story_id>/edit/', views.edit_story, name='edit_story'),
    path('success-stories/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('job-postings/', views.job_postings, name='job_postings'),
    path('job-postings/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('job-postings/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('job-postings/<int:job_id>/applications/', views.view_job_applications, name='view_job_applications'),
    path('events/', views.events_list, name='events_list'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('events/<int:event_id>/registrations/', views.view_event_registrations, name='view_event_registrations'),
    path('registrations/<int:registration_id>/update-status/', views.update_registration_status, name='update_registration_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 