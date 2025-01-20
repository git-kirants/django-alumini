from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('send-message-ajax/<int:conversation_id>/', views.send_message_ajax, name='send_message_ajax'),
    path('api/messages/<int:conversation_id>/', views.get_messages, name='get_messages'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/', views.conversation_list, name='conversation_list'),
    path('report/<int:message_id>/', views.report_message, name='report_message'),
    path('reports/', views.review_reports, name='review_reports'),
    path('reports/<int:report_id>/resolve/', views.resolve_report, name='resolve_report'),
    path('start-conversation/<int:user_id>/', views.start_conversation, name='start_conversation'),
] 