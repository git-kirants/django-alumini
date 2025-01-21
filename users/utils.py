from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Verify your email address'
    
    # Generate verification token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Create verification link
    verification_link = f"http://{current_site.domain}/users/verify/{uid}/{token}/"
    
    # Render email template
    html_message = render_to_string('users/email/verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })
    
    # Create plain text version
    plain_message = f"""
Hi {user.first_name},

Thank you for registering with Alumni Network. Please verify your email address by clicking the link below:

{verification_link}

This link will expire in 24 hours.

Best regards,
Alumni Network Team
    """
    
    if settings.DEBUG:
        print("\nDEBUG: Verification Link:", verification_link)
        return True
        
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False 