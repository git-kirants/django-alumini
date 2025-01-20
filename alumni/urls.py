from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('events/', include('events.urls')),
    path('jobs/', include('jobs.urls')),
    path('charitable/', include('charitable.urls')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('admin-panel/', include('admin_panel.urls')),
    path('success/', include('success.urls', namespace='success')),
    path('messaging/', include('messaging.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
