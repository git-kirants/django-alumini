from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Notification

@shared_task
def send_notification_email_task(notification_id, site_domain=None):
    """
    Celery task to send notification emails asynchronously.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        
        # Check if email notifications are enabled for the user
        if not notification.recipient.notificationpreference.email_notifications:
            return
        
        context = {
            'notification': notification,
            'recipient': notification.recipient,
            'site_url': f'http://{site_domain}' if site_domain else '',
        }

        # Add content URL if available
        if notification.content_object and hasattr(notification.content_object, 'get_absolute_url'):
            context['content_url'] = f"{context['site_url']}{notification.content_object.get_absolute_url()}"

        # Render email templates
        html_message = render_to_string('notifications/email/notification.html', context)
        plain_message = strip_tags(html_message)

        # Send the email
        send_mail(
            subject=notification.title,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient.email],
            html_message=html_message,
            fail_silently=True
        )
        
    except Notification.DoesNotExist:
        pass  # Notification was deleted before email could be sent 