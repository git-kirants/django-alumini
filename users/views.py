from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from messaging.models import Conversation

User = get_user_model()

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
        
    # Check if there's an existing conversation
    conversation = None
    if request.user != profile_user:
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=profile_user
        ).first()
        
    context = {
        'profile_user': profile_user,
        'conversation': conversation,
    }
    return render(request, 'users/profile.html', context)

@login_required
def alumni_directory(request):
    alumni = User.objects.filter(user_type='alumni', is_active=True).order_by('last_name')
    return render(request, 'users/alumni_directory.html', {'alumni': alumni})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:alumni_directory')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/update_profile.html', {'form': form})

@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile.html', {
        'profile_user': profile_user
    })
