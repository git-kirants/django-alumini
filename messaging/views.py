from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from .models import Conversation, Message, MessageReport
from .forms import MessageForm, MessageReportForm
from users.models import User

# Create your views here.

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations
    })

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Security check
    if request.user not in conversation.participants.all():
        messages.error(request, "You don't have access to this conversation.")
        return redirect('messaging:conversation_list')
    
    # Mark messages as read
    conversation.messages.filter(
        sender=conversation.get_other_participant(request.user),
        is_read=False
    ).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Update conversation timestamp
            conversation.save()  # This updates the updated_at field
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'content': message.content,
                        'created_at': message.created_at.strftime('%b %d, %Y, %I:%M %p'),
                        'sender_name': message.sender.get_full_name(),
                    }
                })
            return redirect('messaging:conversation_detail', conversation_id=conversation.id)
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
