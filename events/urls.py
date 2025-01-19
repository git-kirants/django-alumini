from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('<int:pk>/register/', views.event_register, name='event_register'),
    path('<int:pk>/unregister/', views.event_unregister, name='event_unregister'),
    path('<int:pk>/participants/', views.event_participants, name='event_participants'),
    path('my-events/', views.my_events, name='my_events'),
] 