from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from .models import Category, Thread, Reply
from .forms import ThreadForm, ReplyForm, CategoryForm
from notifications.utils import create_notification

def category_list(request):
    categories = Category.objects.annotate(
        thread_count=Count('threads'),
        reply_count=Count('threads__replies')
    )
    return render(request, 'forum/category_list.html', {'categories': categories})

@login_required
@user_passes_test(lambda u: u.is_staff)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('forum:category_list')
    else:
        form = CategoryForm()
    return render(request, 'forum/category_form.html', {'form': form})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    threads = Thread.objects.filter(category=category).order_by('-is_pinned', '-created_at')
    return render(request, 'forum/category_detail.html', {
        'category': category,
        'threads': threads
    })

@login_required
def thread_create(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.category = category
            thread.save()
            messages.success(request, 'Thread created successfully!')
            return redirect('forum:thread_detail', thread_id=thread.id)
    else:
        form = ThreadForm(initial={'category': category})
    return render(request, 'forum/thread_form.html', {'form': form, 'category': category})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    replies = thread.replies.all().order_by('created_at')
    form = ReplyForm()
    
    # Increment view count
    thread.views += 1
    thread.save()
    
    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'replies': replies,
        'form': form
    })

@login_required
def reply_create(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    
    if thread.is_locked and not request.user.is_staff:
        messages.error(request, 'This thread is locked.')
        return redirect('forum:thread_detail', thread_id=thread.id)
        
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.thread = thread
            reply.save()
            
            # Create notification for thread author
            if thread.author != request.user:
                create_notification(
                    recipient=thread.author,
                    notification_type='forum',
                    title=f'New reply to your thread "{thread.title}"',
                    message=f'{request.user.get_full_name() or request.user.username} replied to your thread',
                    related_object=reply,
                    request=request
                )
            
            messages.success(request, 'Reply posted successfully!')
            return redirect('forum:thread_detail', thread_id=thread.id)
    return redirect('forum:thread_detail', thread_id=thread.id)

@user_passes_test(lambda u: u.is_staff)
def thread_pin(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.is_pinned = not thread.is_pinned
    thread.save()
    messages.success(request, f'Thread {"pinned" if thread.is_pinned else "unpinned"} successfully!')
    return redirect('forum:thread_detail', thread_id=thread.id)

@user_passes_test(lambda u: u.is_staff)
def thread_lock(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.is_locked = not thread.is_locked
    thread.save()
    messages.success(request, f'Thread {"locked" if thread.is_locked else "unlocked"} successfully!')
    return redirect('forum:thread_detail', thread_id=thread.id)
