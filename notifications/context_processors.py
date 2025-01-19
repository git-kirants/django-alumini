def notification_count(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(read=False).count()
        return {'unread_notification_count': unread_count}
    return {'unread_notification_count': 0} 