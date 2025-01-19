from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from .models import Notification, NotificationPreference
from .tasks import send_notification_email_task

def create_notification(recipient, notification_type, title, message, related_object=None, request=None):
    """
    Create a notification and queue email if enabled.
    
    Args:
        recipient: User object - the user to receive the notification
        notification_type: str - type of notification ('event', 'job', 'forum', 'system')
        title: str - notification title
        message: str - notification message
        related_object: Model instance - related object (optional)
        request: HTTP request object (optional, for generating absolute URLs in emails)
    """
    # Check user preferences
    try:
        preferences = NotificationPreference.objects.get(user=recipient)
        if notification_type == 'event' and not preferences.events_updates:
            return
        elif notification_type == 'job' and not preferences.job_postings:
            return
        elif notification_type == 'forum' and not preferences.forum_replies:
            return
    except NotificationPreference.DoesNotExist:
        # If no preferences exist, create with defaults
        preferences = NotificationPreference.objects.create(user=recipient)

    # Create the notification
    notification = Notification(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message
    )

    # Add related object if provided
    if related_object:
        content_type = ContentType.objects.get_for_model(related_object)
        notification.content_type = content_type
        notification.object_id = related_object.id

    notification.save()

    # Queue email notification if enabled
    if request:
        site_domain = get_current_site(request).domain
        send_notification_email_task.delay(notification.id, site_domain)

    return notification

def send_bulk_notification(recipients, notification_type, title, message, related_object=None, request=None):
    """
    Send the same notification to multiple users.
    
    Args:
        recipients: QuerySet or list of User objects
        notification_type: str - type of notification
        title: str - notification title
        message: str - notification message
        related_object: Model instance - related object (optional)
        request: HTTP request object (optional, for generating absolute URLs in emails)
    """
    notifications = []
    for recipient in recipients:
        notification = create_notification(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            related_object=related_object,
            request=request
        )
        if notification:
            notifications.append(notification)
    return notifications 