from django.utils import timezone
from django.db.models import Count, Avg, Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from .models import SystemMetric
from users.models import User
from events.models import Event, EventRegistration
from charitable.models import Donation, Fund
from jobs.models import JobPosting, JobApplication
from forum.models import Thread, Reply

def calculate_system_metrics():
    """Calculate and store system metrics"""
    now = timezone.now()
    thirty_days_ago = now - timezone.timedelta(days=30)
    
    metrics = [
        ('user_count', User.objects.count()),
        ('active_users', User.objects.filter(last_login__gte=thirty_days_ago).count()),
        ('event_count', Event.objects.count()),
        ('donation_amount', Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0),
        ('job_count', JobPosting.objects.count()),
    ]
    
    for metric_type, value in metrics:
        SystemMetric.objects.create(metric_type=metric_type, value=value)

def generate_pdf_report(report):
    """Generate PDF report from report data"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add report header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, report.title)
    p.setFont("Helvetica", 12)
    p.drawString(50, 730, f"Generated on: {report.generated_at.strftime('%Y-%m-%d %H:%M')}")
    
    # Add report data
    y = 700
    for key, value in report.data.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 20
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def generate_user_activity_report(start_date, end_date):
    """Generate user activity report data"""
    return {
        'total_users': User.objects.count(),
        'new_users': User.objects.filter(date_joined__range=[start_date, end_date]).count(),
        'active_users': User.objects.filter(last_login__range=[start_date, end_date]).count(),
        'user_types': dict(User.objects.values_list('user_type').annotate(count=Count('id'))),
    }

def generate_event_stats_report(start_date, end_date):
    """Generate event statistics report data"""
    events = Event.objects.filter(date__range=[start_date, end_date])
    return {
        'total_events': events.count(),
        'total_registrations': EventRegistration.objects.filter(event__in=events).count(),
        'event_types': dict(events.values_list('event_type').annotate(count=Count('id'))),
        'avg_attendance': EventRegistration.objects.filter(event__in=events).count() / max(events.count(), 1),
    }

def generate_donation_report(start_date, end_date):
    """Generate donation summary report data"""
    donations = Donation.objects.filter(donation_date__range=[start_date, end_date])
    return {
        'total_donations': donations.count(),
        'total_amount': donations.aggregate(Sum('amount'))['amount__sum'] or 0,
        'avg_donation': donations.aggregate(Avg('amount'))['amount__avg'] or 0,
        'funds': dict(donations.values_list('fund__name').annotate(count=Count('id'))),
    }

def generate_job_stats_report(start_date, end_date):
    """Generate job statistics report data"""
    jobs = JobPosting.objects.filter(created_at__range=[start_date, end_date])
    return {
        'total_jobs': jobs.count(),
        'total_applications': JobApplication.objects.filter(job__in=jobs).count(),
        'job_types': dict(jobs.values_list('job_type').annotate(count=Count('id'))),
        'avg_applications': JobApplication.objects.filter(job__in=jobs).count() / max(jobs.count(), 1),
    }

def generate_system_metrics_report(start_date, end_date):
    """Generate system metrics report data"""
    metrics = SystemMetric.objects.filter(timestamp__range=[start_date, end_date])
    return {
        'user_metrics': dict(metrics.filter(metric_type__in=['user_count', 'active_users']).values_list('metric_type', 'value')),
        'performance_metrics': dict(metrics.filter(metric_type='response_time').values_list('timestamp', 'value')),
        'avg_response_time': metrics.filter(metric_type='response_time').aggregate(Avg('value'))['value__avg'] or 0,
    } 