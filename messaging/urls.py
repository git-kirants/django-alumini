from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('report/<int:message_id>/', views.report_message, name='report_message'),
    path('reports/', views.review_reports, name='review_reports'),
    path('reports/<int:report_id>/resolve/', views.resolve_report, name='resolve_report'),
] 