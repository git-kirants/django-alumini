from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('', views.profile, name='profile'),  # Root path for users/
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('alumni-directory/', views.alumni_directory, name='alumni_directory'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/alumni/', views.register_alumni, name='register_alumni'),
]
