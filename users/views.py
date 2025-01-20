from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm, StudentRegistrationForm, AlumniRegistrationForm
from django.contrib.auth import get_user_model
from messaging.models import Conversation
from django.urls import reverse

User = get_user_model()

# Create your views here.

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'student'  # Set user type to student
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:profile')
    else:
        form = StudentRegistrationForm()

    return render(request, 'users/register_student.html', {'form': form})

def register_alumni(request):
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'alumni'  # Set user type to alumni
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:profile')
    else:
        form = AlumniRegistrationForm()

    return render(request, 'users/register_alumni.html', {'form': form})

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
    
    # Add profile_user to the context
    context = {
        'form': form,
        'profile_user': request.user,
        'conversation': None
    }
    return render(request, 'users/profile.html', context)

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
        # Get all the form data from request.POST
        User.first_name = request.POST.get('first_name')
        User.last_name = request.POST.get('last_name')
        User.email = request.POST.get('email')
        User.graduation_year = request.POST.get('graduation_year')
        User.bio = request.POST.get('bio')
        
        if User.user_type == 'alumni':
            User.current_company = request.POST.get('current_company')
            User.current_job_title = request.POST.get('current_job_title')
            User.years_of_experience = request.POST.get('years_of_experience')
            User.industry = request.POST.get('industry')
            User.portfolio_link = request.POST.get('portfolio_link')
            User.skills = request.POST.get('skills')
            User.certifications = request.POST.get('certifications')
            User.achievements = request.POST.get('achievements')
        
        if 'profile_picture' in request.FILES:
            User.profile_picture = request.FILES['profile_picture']
        
        User.save()
        return redirect('users:profile')
    
    return render(request, 'users/update_profile.html', {'user': request.user})

@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    # Check if there's an existing conversation (like in your profile_view)
    conversation = None
    if request.user != profile_user:
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=profile_user
        ).first()
    
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'conversation': conversation
    })

def some_view(request):
    # Change this
    return redirect('alumni_directory')
    
    # To this
    return redirect('users:alumni_directory')
    # Or use reverse()
    return redirect(reverse('users:alumni_directory'))


def home(request):
    return render(request, 'home.html')