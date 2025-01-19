from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags

def send_notification_email(notification, request=None):
    """
    Send an email notification to a user.
    
    Args:
        notification: Notification object
        request: HTTP request object (optional, for generating absolute URLs)
    """
    if not notification.recipient.notificationpreference.email_notifications:
        return

    context = {
        'notification': notification,
        'recipient': notification.recipient,
    }

    # Add absolute URL to the related content if available
    if notification.content_object and request:
        current_site = get_current_site(request)
        if hasattr(notification.content_object, 'get_absolute_url'):
            context['content_url'] = f'http://{current_site.domain}{notification.content_object.get_absolute_url()}'

    # Render email templates
    html_message = render_to_string('notifications/email/notification.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject=notification.title,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[notification.recipient.email],
        html_message=html_message,
        fail_silently=True
    ) 