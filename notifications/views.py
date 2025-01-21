from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Notification, NotificationPreference
from .forms import NotificationPreferenceForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.cache import cache
from django.shortcuts import render
from celery.app.control import Control
from .tasks import send_notification_email_task

# Create your views here.

@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    unread_notifications_exist = notifications.filter(read=False).exists()
    
    context = {
        'notifications': notifications,
        'unread_notifications_exist': unread_notifications_exist,
    }
    return render(request, 'notifications/notification_list.html', context)

@login_required
def notification_preferences(request):
    preference, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated successfully!')
            return redirect('notifications:preferences')
    else:
        form = NotificationPreferenceForm(instance=preference)
    
    return render(request, 'notifications/preferences.html', {'form': form})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def mark_all_as_read(request):
    request.user.notifications.filter(read=False).update(read=True)
    return JsonResponse({'status': 'success'})

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    return JsonResponse({'status': 'success'})

@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        request.user.notifications.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)

@staff_member_required
def task_monitor(request):
    # Get Celery inspector
    control = Control(app=send_notification_email_task.app)
    i = control.inspect()
    
    # Get active, reserved and scheduled tasks
    active_tasks = i.active() or {}
    reserved_tasks = i.reserved() or {}
    scheduled_tasks = i.scheduled() or {}
    
    # Get today's metrics
    metrics_key = f'celery_metrics_{timezone.now().date()}'
    metrics = cache.get(metrics_key, {
        'total': 0,
        'success': 0,
        'failure': 0,
        'revoked': 0,
        'retry': 0,
        'avg_runtime': 0
    })
    
    context = {
        'active_tasks': active_tasks,
        'reserved_tasks': reserved_tasks,
        'scheduled_tasks': scheduled_tasks,
        'metrics': metrics,
        'workers_online': bool(active_tasks),
    }
    
    return render(request, 'notifications/task_monitor.html', context)
