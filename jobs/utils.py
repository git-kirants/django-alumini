from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_application_notification(application):
    # Email to employer
    employer_context = {
        'job_title': application.job.title,
        'applicant_name': application.applicant.get_full_name(),
        'application_id': application.id,
    }
    
    employer_html = render_to_string('jobs/emails/new_application.html', employer_context)
    
    if settings.DEBUG:
        print(f"[DEBUG] New application notification would be sent to {application.job.posted_by.email}")
        print(employer_html)
    else:
        send_mail(
            subject=f'New application for {application.job.title}',
            message=employer_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.job.posted_by.email],
            html_message=employer_html
        )

def send_status_update_notification(application):
    applicant_context = {
        'job_title': application.job.title,
        'company': application.job.company,
        'status': application.get_status_display(),
    }
    
    applicant_html = render_to_string('jobs/emails/status_update.html', applicant_context)
    
    if settings.DEBUG:
        print(f"[DEBUG] Status update notification would be sent to {application.applicant.email}")
        print(applicant_html)
    else:
        send_mail(
            subject=f'Status update for your application at {application.job.company}',
            message=applicant_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.applicant.email],
            html_message=applicant_html
        ) 