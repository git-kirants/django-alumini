from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import SuccessStory, Comment
from .forms import SuccessStoryForm, CommentForm, StoryReviewForm

def story_list(request):
    stories = SuccessStory.objects.filter(status='approved')
    return render(request, 'success/story_list.html', {'stories': stories})

@login_required
def story_create(request):
    if request.method == 'POST':
        form = SuccessStoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            messages.success(request, 'Your success story has been submitted for review!')
            return redirect('success:my_stories')
    else:
        form = SuccessStoryForm()
    return render(request, 'success/story_form.html', {'form': form, 'action': 'Share'})

@login_required
def story_detail(request, story_id):
    story = get_object_or_404(SuccessStory, id=story_id)
    if story.status != 'approved' and story.author != request.user and not request.user.is_staff:
        messages.error(request, 'This story is not available.')
        return redirect('success:story_list')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.story = story
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('success:story_detail', story_id=story.id)
    else:
        form = CommentForm()
    
    return render(request, 'success/story_detail.html', {
        'story': story,
        'comment_form': form
    })

@login_required
def my_stories(request):
    stories = SuccessStory.objects.filter(author=request.user)
    return render(request, 'success/my_stories.html', {'stories': stories})

@login_required
@user_passes_test(lambda u: u.is_staff)
def review_stories(request):
    stories = SuccessStory.objects.filter(status='pending')
    return render(request, 'success/review_stories.html', {'stories': stories})

@login_required
@user_passes_test(lambda u: u.is_staff)
def review_story(request, story_id):
    story = get_object_or_404(SuccessStory, id=story_id)
    if request.method == 'POST':
        form = StoryReviewForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save(commit=False)
            story.reviewed_by = request.user
            story.reviewed_at = timezone.now()
            story.save()
            messages.success(request, 'Story review completed!')
            return redirect('success:review_stories')
    else:
        form = StoryReviewForm(instance=story)
    return render(request, 'success/review_story.html', {
        'form': form,
        'story': story
    })
