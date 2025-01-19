from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/thread/create/', views.thread_create, name='thread_create'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/reply/', views.reply_create, name='reply_create'),
    path('thread/<int:thread_id>/pin/', views.thread_pin, name='thread_pin'),
    path('thread/<int:thread_id>/lock/', views.thread_lock, name='thread_lock'),
] 