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

# Create your views here.

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations
    })

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender_id': message.sender.id,
                    'created_at': message.created_at.isoformat()
                }
            })
    else:
        form = MessageForm()
    
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'form': form
    })

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Check if conversation already exists
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if conversation:
        return redirect('messaging:conversation_detail', conversation_id=conversation.id)
    
    # Create new conversation
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
                'created_at': message.created_at.isoformat(),
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
        after_id = request.GET.get('after', 0)
        
        messages = conversation.messages.filter(id__gt=after_id).order_by('created_at')
        
        messages_data = [{
            'id': message.id,
            'content': message.content,
            'sender_id': message.sender.id,
            'created_at': message.created_at.isoformat(),
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
