from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm, StudentRegistrationForm, AlumniRegistrationForm
from django.contrib.auth import get_user_model
from messaging.models import Conversation
from django.urls import reverse, reverse_lazy
from django.views.decorators.cache import never_cache
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.core.mail.backends.console import EmailBackend
from django.contrib.auth.views import PasswordResetView

User = get_user_model()

# Create your views here.

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(request, user)
            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('users:login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'users/register_student.html', {'form': form})

def register_alumni(request):
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'alumni'
            user.email_verified = False  # Set email as unverified initially
            user.save()
            send_verification_email(request, user)  # Send verification email
            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('users:login')
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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.email_verified:
                messages.error(request, 'Please verify your email address before logging in. Check your inbox for the verification link.')
                return redirect('users:login')
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@never_cache
def logout_view(request):
    logout(request)
    response = redirect('users:login')
    # Prevent caching of authenticated pages
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    messages.success(request, 'You have been logged out.')
    return response

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
    alumni = User.objects.filter(
        user_type='alumni',
        is_active=True,
        email_verified=True
    ).order_by('last_name')
    return render(request, 'users/alumni_directory.html', {'alumni': alumni})

@login_required
def update_profile(request):
    if request.method == 'POST':
        # Get the current user instance
        user = request.user
        
        # Update user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        # Handle graduation_year - convert to int or set to None if empty
        graduation_year = request.POST.get('graduation_year')
        user.graduation_year = int(graduation_year) if graduation_year else None
        
        user.bio = request.POST.get('bio')
        
        if user.user_type == 'alumni':
            user.current_company = request.POST.get('current_company')
            user.current_job_title = request.POST.get('current_job_title')
            
            # Handle years_of_experience - convert to int or set to 0 if empty
            years_exp = request.POST.get('years_of_experience')
            user.years_of_experience = int(years_exp) if years_exp else 0
            
            user.industry = request.POST.get('industry')
            user.portfolio_link = request.POST.get('portfolio_link')
            user.skills = request.POST.get('skills')
            user.certifications = request.POST.get('certifications')
            user.achievements = request.POST.get('achievements')
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        try:
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
        except ValueError as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
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

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return render(request, 'users/email_verified.html', {'success': True})
        else:
            return render(request, 'users/email_verified.html', {'success': False})
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'users/email_verified.html', {'success': False})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/email/password_reset_email.html'
    html_email_template_name = 'users/email/password_reset_email.html'
    subject_template_name = 'users/email/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        form.save(
            use_https=self.request.is_secure(),
            from_email=None,
            request=self.request,
            email_template_name=self.email_template_name,
            html_email_template_name=self.html_email_template_name,
            subject_template_name=self.subject_template_name
        )
        return super().form_valid(form)

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'