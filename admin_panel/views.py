from django.shortcuts import render, redirect, get_object_or_404
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
from .models import AdminReport, SystemMetric, Report
from .utils import (
    generate_pdf_report,
    calculate_system_metrics,
    generate_user_activity_report,
    generate_event_stats_report,
    generate_donation_report,
    generate_job_stats_report,
    generate_system_metrics_report,
    get_system_load,
    get_memory_usage,
    get_cpu_usage,
    get_disk_usage,
    get_network_traffic,
    get_db_query_rate,
    get_cache_hit_rate,
    get_error_rate,
    get_avg_response_time,
    get_metric_change,
    get_user_metrics
)
from django.http import HttpResponse, FileResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
import json
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

User = get_user_model()

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

@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Create report instance
        report = Report.objects.create(
            title=f"{report_type.replace('_', ' ').title()} Report",
            report_type=report_type,
            generated_by=request.user,
            start_date=start_date,
            end_date=end_date
        )
        
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
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(report, data)
        
        # Save PDF file
        filename = f"report_{report.id}.pdf"
        report.file_path.save(filename, ContentFile(pdf_buffer.read()))
        
        messages.success(request, 'Report generated successfully.')
        return redirect('admin_panel:view_report', report_id=report.id)
    
    recent_reports = Report.objects.all().order_by('-created_at')[:10]
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
    if request.method == 'POST':
        # Refresh metrics
        calculate_system_metrics()
        messages.success(request, 'System metrics have been refreshed.')
        return redirect('admin_panel:system_metrics')

    # Get the latest metrics
    metrics = {
        'user_metrics': get_user_metrics(),
        'performance_metrics': {
            'system_load': get_system_load(),
            'avg_response_time': get_avg_response_time(),
            'memory_usage': get_memory_usage(),
            'cpu_usage': get_cpu_usage(),
            'cpu_usage_change': get_metric_change('cpu_usage'),
            'db_query_rate': get_db_query_rate(),
            'db_query_rate_change': get_metric_change('db_query_rate'),
            'cache_hit_rate': get_cache_hit_rate(),
            'cache_hit_rate_change': get_metric_change('cache_hit_rate'),
            'error_rate': get_error_rate(),
            'error_rate_change': get_metric_change('error_rate'),
            'network_traffic': get_network_traffic(),
            'network_traffic_change': get_metric_change('network_traffic'),
            'disk_usage': get_disk_usage(),
            'disk_usage_change': get_metric_change('disk_usage'),
        }
    }
    
    return render(request, 'admin_panel/system_metrics.html', {'metrics': metrics})

@login_required
@user_passes_test(lambda u: u.is_staff)
def view_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.file_path:
        return FileResponse(report.file_path.open('rb'), content_type='application/pdf')
    return HttpResponse("Report not found", status=404)

@login_required
@user_passes_test(lambda u: u.is_staff)
def download_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.file_path:
        response = FileResponse(report.file_path.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{report.title}.pdf"'
        return response
    return HttpResponse("Report not found", status=404)

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Update user information
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.user_type = request.POST.get('user_type', 'student')
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        
        try:
            user.save()
            messages.success(request, f'User {user.username} has been updated successfully.')
            return redirect('admin_panel:user_management')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return render(request, 'admin_panel/edit_user.html', {'edit_user': user})

@require_POST
@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_user_status(request, user_id):
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, id=user_id)
        
        # Don't allow deactivating your own account
        if user == request.user:
            return JsonResponse({
                'status': 'error',
                'message': 'You cannot modify your own account status.'
            }, status=403)
        
        user.is_active = data.get('is_active', False)
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'User {user.username} has been {"activated" if user.is_active else "deactivated"} successfully.'
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'User not found.'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
