from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('alumni-directory/', views.alumni_directory, name='alumni_directory'),
    path('profile/update/', views.update_profile, name='update_profile'),
]
