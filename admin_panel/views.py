from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from django.core.paginator import Paginator
from datetime import timedelta
from users.models import User
from events.models import Event, EventRegistration
from charitable.models import Donation, Fund
from jobs.models import JobPosting, JobApplication
from forum.models import Thread, Reply
from .models import AdminReport, SystemMetric
from .utils import generate_pdf_report, calculate_system_metrics, generate_user_activity_report, generate_event_stats_report, generate_donation_report, generate_job_stats_report, generate_system_metrics_report

# Create your views here.

@staff_member_required
def admin_dashboard(request):
    # Get date range for filtering
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Gather statistics
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(last_login__gte=start_date).count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(date__gte=end_date).count(),
        'total_donations': Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_jobs': JobPosting.objects.count(),
        'active_jobs': JobPosting.objects.filter(deadline__gte=end_date).count(),
    }
    
    # Get recent activities
    recent_activities = {
        'new_users': User.objects.order_by('-date_joined')[:5],
        'recent_events': Event.objects.order_by('-created_at')[:5],
        'recent_donations': Donation.objects.order_by('-donation_date')[:5],
    }
    
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_activities': recent_activities,
    })

@staff_member_required
def generate_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Generate report data based on type
        if report_type == 'user_activity':
            data = generate_user_activity_report(start_date, end_date)
        elif report_type == 'event_stats':
            data = generate_event_stats_report(start_date, end_date)
        elif report_type == 'donation_summary':
            data = generate_donation_report(start_date, end_date)
        elif report_type == 'job_stats':
            data = generate_job_stats_report(start_date, end_date)
        elif report_type == 'system_metrics':
            data = generate_system_metrics_report(start_date, end_date)
        else:
            messages.error(request, 'Invalid report type selected.')
            return redirect('admin_panel:generate_report')
        
        # Create report record
        report = AdminReport.objects.create(
            title=f"{report_type.replace('_', ' ').title()} Report",
            report_type=report_type,
            generated_by=request.user,
            date_range_start=start_date,
            date_range_end=end_date,
            data=data
        )
        
        # Generate PDF
        pdf_file = generate_pdf_report(report)
        
        messages.success(request, 'Report generated successfully!')
        return redirect('admin_panel:generate_report')
    
    # Get recent reports for display
    recent_reports = AdminReport.objects.all()[:10]
    return render(request, 'admin_panel/generate_report.html', {'recent_reports': recent_reports})

@staff_member_required
def user_management(request):
    users = User.objects.all().order_by('-date_joined')
    user_type = request.GET.get('user_type')
    search = request.GET.get('search')
    
    if user_type:
        users = users.filter(user_type=user_type)
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    return render(request, 'admin_panel/user_management.html', {'users': users})

@staff_member_required
def system_metrics(request):
    # Calculate and store current metrics
    calculate_system_metrics()
    
    # Get metrics for display
    metrics = {
        'user_metrics': SystemMetric.objects.filter(metric_type__in=['user_count', 'active_users']),
        'event_metrics': SystemMetric.objects.filter(metric_type='event_count'),
        'donation_metrics': SystemMetric.objects.filter(metric_type='donation_amount'),
        'performance_metrics': SystemMetric.objects.filter(metric_type='response_time'),
    }
    
    return render(request, 'admin_panel/system_metrics.html', {'metrics': metrics})
