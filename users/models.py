from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('alumni', 'Alumni'),
        ('student', 'Student'),
    )
    
    INDUSTRY_CHOICES = (
        ('it', 'Information Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('consulting', 'Consulting'),
        ('marketing', 'Marketing'),
        ('other', 'Other')
    )

    AVAILABILITY_CHOICES = (
        ('available', 'Available for Mentorship'),
        ('limited', 'Limited Availability'),
        ('unavailable', 'Not Available'),
    )
    
    # Basic Fields
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    # Professional Information
    current_job_title = models.CharField(max_length=100, blank=True)
    current_company = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    skills = models.TextField(help_text="Enter skills separated by commas", blank=True)
    achievements = models.TextField(blank=True)
    certifications = models.TextField(help_text="Enter certifications separated by commas", blank=True)
    linkedin_profile = models.URLField(max_length=200, blank=True)
    portfolio_link = models.URLField(max_length=200, blank=True)
    mentorship_availability = models.CharField(
        max_length=20, 
        choices=AVAILABILITY_CHOICES,
        blank=True
    )

    def clean(self):
        # Skip validation for admin users
        if self.user_type == 'admin':
            return
        
        if self.user_type == 'alumni':
            required_fields = [
                'current_job_title',
                'current_company',
                'industry',
                'years_of_experience',
                'skills',
                'mentorship_availability'
            ]
            
            missing_fields = [
                field for field in required_fields 
                if not getattr(self, field)
            ]
            
            if missing_fields:
                raise ValidationError(
                    f"As an alumni, the following fields are required: {', '.join(missing_fields)}"
                )
        elif self.user_type == 'student':
            # Clear professional fields if they were filled
            professional_fields = [
                'current_job_title',
                'current_company',
                'industry',
                'years_of_experience',
                'skills',
                'mentorship_availability'
            ]
            for field in professional_fields:
                setattr(self, field, '')
            self.years_of_experience = 0

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
