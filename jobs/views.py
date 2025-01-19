from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import JobPosting, JobApplication
from .forms import JobPostingForm, JobApplicationForm, ApplicationStatusForm
from .utils import send_application_notification, send_status_update_notification
from notifications.utils import send_bulk_notification
from users.models import User

def job_list(request):
    jobs = JobPosting.objects.filter(
        is_active=True,
        deadline__gt=timezone.now()
    ).order_by('-created_at')
    
    # Search and filter
    search_query = request.GET.get('search', '')
    job_type = request.GET.get('type', '')
    experience = request.GET.get('experience', '')
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    if experience:
        jobs = jobs.filter(experience_level=experience)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'search_query': search_query,
        'job_type': job_type,
        'experience': experience,
    })

@login_required
def job_create(request):
    if not (request.user.is_staff or request.user.user_type == 'alumni'):
        messages.error(request, "You don't have permission to post jobs.")
        return redirect('job_list')
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            
            # Notify all users about new job posting
            users = User.objects.filter(is_active=True)
            send_bulk_notification(
                recipients=users,
                notification_type='job',
                title=f'New Job Posting: {job.title}',
                message=f'New job opportunity at {job.company}: {job.title}',
                related_object=job
            )
            
            messages.success(request, 'Job posting created successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostingForm()
    
    return render(request, 'jobs/job_form.html', {
        'form': form,
        'action': 'Create'
    })

def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    user_has_applied = False
    
    if request.user.is_authenticated:
        user_has_applied = JobApplication.objects.filter(
            job=job,
            applicant=request.user
        ).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'user_has_applied': user_has_applied
    })

@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    
    if not (request.user.is_staff or request.user == job.posted_by):
        messages.error(request, "You don't have permission to edit this job posting.")
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posting updated successfully!')
            return redirect('job_detail', pk=pk)
    else:
        form = JobPostingForm(instance=job)
    
    return render(request, 'jobs/job_form.html', {
        'form': form,
        'action': 'Edit',
        'job': job
    })

@login_required
def job_apply(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    
    if job.is_expired:
        messages.error(request, "This job posting has expired.")
        return redirect('job_detail', pk=pk)
    
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.error(request, "You have already applied for this position.")
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            send_application_notification(application)
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = JobApplicationForm()
    
    return render(request, 'jobs/job_apply.html', {
        'form': form,
        'job': job
    })

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        applicant=request.user
    ).order_by('-applied_at')
    
    return render(request, 'jobs/my_applications.html', {
        'applications': applications
    })

@login_required
def manage_applications(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    
    if not (request.user.is_staff or request.user == job.posted_by):
        messages.error(request, "You don't have permission to manage applications.")
        return redirect('job_detail', pk=pk)
    
    applications = JobApplication.objects.filter(job=job).order_by('-applied_at')
    
    return render(request, 'jobs/manage_applications.html', {
        'job': job,
        'applications': applications
    })

@login_required
def update_application_status(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    
    if not (request.user.is_staff or request.user == application.job.posted_by):
        messages.error(request, "You don't have permission to update application status.")
        return redirect('job_detail', pk=application.job.pk)
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            old_status = application.status
            application = form.save()
            if old_status != application.status:
                send_status_update_notification(application)
            messages.success(request, 'Application status updated successfully!')
            return redirect('manage_applications', pk=application.job.pk)
    else:
        form = ApplicationStatusForm(instance=application)
    
    return render(request, 'jobs/update_application_status.html', {
        'form': form,
        'application': application
    })

@login_required
def my_job_posts(request):
    jobs = JobPosting.objects.filter(
        posted_by=request.user
    ).order_by('-created_at')
    
    return render(request, 'jobs/my_job_posts.html', {
        'jobs': jobs
    })
