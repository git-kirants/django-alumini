from django.urls import path
from . import views

app_name = 'success'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('create/', views.story_create, name='story_create'),
    path('<int:story_id>/', views.story_detail, name='story_detail'),
    path('my-stories/', views.my_stories, name='my_stories'),
    path('review/', views.review_stories, name='review_stories'),
    path('review/<int:story_id>/', views.review_story, name='review_story'),
] 