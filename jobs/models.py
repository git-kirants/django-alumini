from django.db import models
from django.utils import timezone
from users.models import User

class JobPosting(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]

    EXPERIENCE_LEVELS = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead/Manager'),
        ('executive', 'Executive'),
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    description = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField(blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    salary_range = models.CharField(max_length=100, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_postings')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    remote_work = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        if self.deadline is None:
            return False
        return timezone.now().date() > self.deadline

    class Meta:
        ordering = ['-created_at']

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offer Extended'),
        ('accepted', 'Offer Accepted'),
        ('rejected', 'Application Rejected'),
        ('withdrawn', 'Application Withdrawn'),
    )

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['job', 'applicant']

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title}"
