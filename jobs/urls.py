from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('<int:pk>/apply/', views.job_apply, name='job_apply'),
    path('my-posts/', views.my_job_posts, name='my_job_posts'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:pk>/applications/', views.manage_applications, name='manage_applications'),
    path('application/<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
] 