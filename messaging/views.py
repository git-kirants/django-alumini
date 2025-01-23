from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from .models import Conversation, Message, MessageReport
from .forms import MessageForm, MessageReportForm
from users.models import User
from django.views.decorators.http import require_POST, require_http_methods
import json
from django.utils.timezone import localtime

# Create your views here.

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all().prefetch_related(
        'participants',
        'messages'
    ).order_by('-updated_at')

    # Add request user to each conversation for template context
    for conversation in conversations:
        conversation._request_user = request.user

    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations
    })

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    conversation._request_user = request.user
    
    # Mark all unread messages in this conversation as read
    Message.objects.filter(
        conversation=conversation,
        sender__in=conversation.participants.exclude(id=request.user.id),
        is_read=False
    ).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'id': message.id,
                        'content': message.content,
                        'timestamp': localtime(message.created_at).strftime('%-I:%M %p'),  # Format: 9:41 PM
                        'is_sender': True
                    }
                })
            return redirect('messaging:conversation_detail', conversation_id=conversation_id)
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'error': form.errors}, status=400)
    
    messages = conversation.messages.all().order_by('created_at')
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': MessageForm()
    })

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Check if a conversation already exists between these users
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    # If no conversation exists, create a new one
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)

@login_required
def report_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    if request.method == 'POST':
        form = MessageReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.message = message
            report.reported_by = request.user
            report.save()
            messages.success(request, 'Message reported successfully.')
            return redirect('messaging:conversation_detail', conversation_id=message.conversation.id)
    else:
        form = MessageReportForm()
    
    return render(request, 'messaging/report_message.html', {
        'form': form,
        'message': message
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def review_reports(request):
    reports = MessageReport.objects.filter(resolved=False).order_by('-created_at')
    return render(request, 'messaging/review_reports.html', {'reports': reports})

@login_required
@user_passes_test(lambda u: u.is_staff)
def resolve_report(request, report_id):
    report = get_object_or_404(MessageReport, id=report_id)
    report.resolved = True
    report.resolved_by = request.user
    report.resolved_at = timezone.now()
    report.save()
    messages.success(request, 'Report resolved successfully.')
    return redirect('messaging:review_reports')

@require_http_methods(["POST"])
def send_message_ajax(request, conversation_id):
    try:
        # Get the conversation or return 404
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Parse the JSON data from request body
        data = json.loads(request.body)
        content = data.get('content')
        
        if not content:
            return JsonResponse({
                'status': 'error',
                'message': 'Message content is required'
            }, status=400)
        
        # Create new message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        # Return the message data
        return JsonResponse({
            'status': 'success',
            'message': {
                'id': message.id,
                'content': message.content,
                'sender_id': message.sender.id,
                'created_at': localtime(message.created_at).isoformat(),
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def get_messages(request, conversation_id):
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        last_message_id = request.GET.get('after', '0')
        
        # Convert to int, defaulting to 0 if invalid
        try:
            last_message_id = int(last_message_id)
        except (ValueError, TypeError):
            last_message_id = 0
        
        # Get messages after the last seen message ID, ordered by created_at
        messages = conversation.messages.filter(
            id__gt=last_message_id
        ).select_related('sender').order_by('created_at')
        
        messages_data = [{
            'id': message.id,
            'content': message.content,
            'sender_id': message.sender.id,
            'sender_name': message.sender.get_full_name() or message.sender.username,
            'timestamp': localtime(message.created_at).strftime('%-I:%M %p'),  # Format: 9:41 PM
            'is_sender': message.sender_id == request.user.id
        } for message in messages]
        
        return JsonResponse({
            'status': 'success',
            'messages': messages_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
