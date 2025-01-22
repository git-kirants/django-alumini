from django import template
from django.db.models import Q
from messaging.models import Message, Conversation

register = template.Library()

@register.inclusion_tag('messaging/tags/message_badge.html')
def message_badge(user=None):
    if not user or not user.is_authenticated:
        return {'unread_count': 0}
    
    # Get all conversations where the user is a participant
    conversations = Conversation.objects.filter(participants=user)
    
    # Get unread messages from these conversations where the user is not the sender
    unread_count = Message.objects.filter(
        conversation__in=conversations,
        is_read=False
    ).exclude(sender=user).count()
    
    return {'unread_count': unread_count}
