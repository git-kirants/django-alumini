from django import template
from django.template.loader import render_to_string
from notifications.models import Notification

register = template.Library()

@register.simple_tag(takes_context=True)
def get_unread_notification_count(context):
    user = context['user']
    if user.is_authenticated:
        return Notification.objects.filter(recipient=user, read=False).count()
    return 0

@register.inclusion_tag('notifications/notification_badge.html', takes_context=True)
def notification_badge(context):
    user = context['user']
    unread_count = 0
    if user.is_authenticated:
        unread_count = Notification.objects.filter(recipient=user, read=False).count()
    return {'unread_count': unread_count}
