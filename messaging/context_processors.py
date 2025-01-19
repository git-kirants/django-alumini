from .models import Message

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(
            conversation__participants=request.user,
            sender__in=request.user.conversations.values_list('participants', flat=True),
            is_read=False
        ).exclude(sender=request.user).count()
        return {'unread_message_count': count}
    return {'unread_message_count': 0} 