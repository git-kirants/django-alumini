from django.utils import timezone
from django.db.models import Count, Q
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from users.models import User
from events.models import Event, EventRegistration
from jobs.models import JobPosting, JobApplication
from charitable.models import CharitableCause, Donation
from success.models import SuccessStory
import datetime

def generate_user_activity_report(start_date, end_date):
    """Generate detailed user activity report data"""
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__range=[start_date, end_date]).count()
    new_users = User.objects.filter(date_joined__range=[start_date, end_date]).count()
    
    # User type distribution
    alumni_count = User.objects.filter(is_alumni=True).count()
    student_count = User.objects.filter(is_student=True).count()
    faculty_count = User.objects.filter(is_faculty=True).count()
    
    return {
        'title': 'User Activity Report',
        'period': f'{start_date} to {end_date}',
        'sections': [
            {
                'name': 'User Overview',
                'data': [
                    ('Total Users', total_users),
                    ('Active Users in Period', active_users),
                    ('New Users in Period', new_users),
                ]
            },
            {
                'name': 'User Distribution',
                'data': [
                    ('Alumni', alumni_count),
                    ('Students', student_count),
                    ('Faculty', faculty_count),
                ]
            }
        ]
    }

def generate_event_stats_report(start_date, end_date):
    """Generate comprehensive event statistics report data"""
    events = Event.objects.filter(date__range=[start_date, end_date])
    total_events = events.count()
    
    # Event type distribution
    event_types = events.values('event_type').annotate(count=Count('id'))
    
    # Registration statistics
    total_registrations = EventRegistration.objects.filter(
        event__date__range=[start_date, end_date]
    ).count()
    
    # Status distribution
    registration_status = EventRegistration.objects.filter(
        event__date__range=[start_date, end_date]
    ).values('status').annotate(count=Count('id'))
    
    # Online vs Physical events
    online_events = events.filter(is_online=True).count()
    physical_events = events.filter(is_online=False).count()
    
    # Attendance rates
    attended = EventRegistration.objects.filter(
        event__date__range=[start_date, end_date],
        status='attended'
    ).count()
    
    # Event capacity utilization
    total_capacity = events.aggregate(total=Sum('capacity'))['total'] or 0
    utilization = (total_registrations / total_capacity * 100) if total_capacity > 0 else 0
    
    return {
        'title': 'Event Statistics Report',
        'period': f'{start_date} to {end_date}',
        'sections': [
            {
                'name': 'Event Overview',
                'data': [
                    ('Total Events', total_events),
                    ('Online Events', online_events),
                    ('Physical Events', physical_events),
                ]
            },
            {
                'name': 'Event Types',
                'data': [(type_data['event_type'], type_data['count']) for type_data in event_types]
            },
            {
                'name': 'Registration Statistics',
                'data': [
                    ('Total Registrations', total_registrations),
                    ('Total Capacity', total_capacity),
                    ('Capacity Utilization', f'{utilization:.1f}%'),
                ]
            },
            {
                'name': 'Registration Status',
                'data': [(status['status'], status['count']) for status in registration_status]
            },
            {
                'name': 'Attendance',
                'data': [
                    ('Attended', attended),
                    ('Attendance Rate', f'{(attended/total_registrations*100):.1f}%' if total_registrations > 0 else '0%'),
                ]
            }
        ]
    }

def generate_job_stats_report(start_date, end_date):
    """Generate detailed job statistics report data"""
    jobs = JobPosting.objects.filter(posted_date__range=[start_date, end_date])
    total_jobs = jobs.count()
    
    # Job type distribution
    job_types = jobs.values('job_type').annotate(count=Count('id'))
    
    # Application statistics
    applications = JobApplication.objects.filter(
        job_posting__posted_date__range=[start_date, end_date]
    )
    total_applications = applications.count()
    
    # Status distribution
    application_status = applications.values('status').annotate(count=Count('id'))
    
    # Company distribution
    company_jobs = jobs.values('company').annotate(count=Count('id'))
    
    return {
        'title': 'Job Statistics Report',
        'period': f'{start_date} to {end_date}',
        'sections': [
            {
                'name': 'Job Overview',
                'data': [
                    ('Total Job Postings', total_jobs),
                    ('Total Applications', total_applications),
                    ('Average Applications per Job', f'{total_applications/total_jobs:.1f}' if total_jobs > 0 else '0'),
                ]
            },
            {
                'name': 'Job Types',
                'data': [(type_data['job_type'], type_data['count']) for type_data in job_types]
            },
            {
                'name': 'Application Status',
                'data': [(status['status'], status['count']) for status in application_status]
            },
            {
                'name': 'Top Companies',
                'data': [(comp['company'], comp['count']) for comp in company_jobs[:5]]
            }
        ]
    }

def generate_donation_report(start_date, end_date):
    """Generate comprehensive donation report data"""
    donations = Donation.objects.filter(date__range=[start_date, end_date])
    total_donations = donations.count()
    total_amount = donations.aggregate(total=Sum('amount'))['total'] or 0
    
    # Cause-wise distribution
    cause_donations = donations.values('cause__title').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    # Donor statistics
    unique_donors = donations.values('donor').distinct().count()
    avg_donation = total_amount / total_donations if total_donations > 0 else 0
    
    # Status distribution
    status_dist = donations.values('status').annotate(count=Count('id'))
    
    return {
        'title': 'Donation Summary Report',
        'period': f'{start_date} to {end_date}',
        'sections': [
            {
                'name': 'Donation Overview',
                'data': [
                    ('Total Donations', total_donations),
                    ('Total Amount', f'₹{total_amount:,.2f}'),
                    ('Unique Donors', unique_donors),
                    ('Average Donation', f'₹{avg_donation:,.2f}'),
                ]
            },
            {
                'name': 'Cause Distribution',
                'data': [
                    (cause['cause__title'], 
                     f'₹{cause["total"]:,.2f} ({cause["count"]} donations)') 
                    for cause in cause_donations
                ]
            },
            {
                'name': 'Status Distribution',
                'data': [(status['status'], status['count']) for status in status_dist]
            }
        ]
    }

def generate_system_metrics_report(start_date, end_date):
    """Generate system-wide metrics report data"""
    # User engagement
    active_users = User.objects.filter(last_login__range=[start_date, end_date]).count()
    total_users = User.objects.count()
    
    # Content metrics
    new_stories = SuccessStory.objects.filter(created_at__range=[start_date, end_date]).count()
    new_events = Event.objects.filter(created_at__range=[start_date, end_date]).count()
    new_jobs = JobPosting.objects.filter(posted_date__range=[start_date, end_date]).count()
    new_causes = CharitableCause.objects.filter(created_at__range=[start_date, end_date]).count()
    
    # Activity metrics
    event_registrations = EventRegistration.objects.filter(
        registration_date__range=[start_date, end_date]
    ).count()
    job_applications = JobApplication.objects.filter(
        applied_date__range=[start_date, end_date]
    ).count()
    donations = Donation.objects.filter(date__range=[start_date, end_date]).count()
    
    return {
        'title': 'System Metrics Report',
        'period': f'{start_date} to {end_date}',
        'sections': [
            {
                'name': 'User Engagement',
                'data': [
                    ('Active Users', active_users),
                    ('Total Users', total_users),
                    ('Activity Rate', f'{(active_users/total_users*100):.1f}%' if total_users > 0 else '0%'),
                ]
            },
            {
                'name': 'New Content',
                'data': [
                    ('Success Stories', new_stories),
                    ('Events', new_events),
                    ('Job Postings', new_jobs),
                    ('Charitable Causes', new_causes),
                ]
            },
            {
                'name': 'User Activities',
                'data': [
                    ('Event Registrations', event_registrations),
                    ('Job Applications', job_applications),
                    ('Donations Made', donations),
                ]
            }
        ]
    }

def generate_pdf_report(report_obj, data):
    """Generate a PDF report with the provided data"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1a56db'),
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#374151'),
    )
    
    # Add title
    story.append(Paragraph(data['title'], title_style))
    story.append(Paragraph(f"Period: {data['period']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Add sections
    for section in data['sections']:
        story.append(Paragraph(section['name'], section_style))
        
        # Create table for section data
        table_data = [[Paragraph(str(key), styles['Normal']), 
                      Paragraph(str(value), styles['Normal'])] 
                     for key, value in section['data']]
        
        if table_data:
            table = Table(table_data, colWidths=[300, 200])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E5E7EB')),
            ]))
            story.append(table)
        
        story.append(Spacer(1, 20))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
