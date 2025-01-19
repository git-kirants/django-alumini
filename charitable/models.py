from django.db import models
from django.conf import settings
from django.utils import timezone

class Fund(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def __str__(self):
        return self.name

class Donation(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)
    donation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.donor.username} - ${self.amount} to {self.fund.name}"

class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    financial_need = models.TextField()
    achievements = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount_awarded = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    applied_date = models.DateTimeField(default=timezone.now)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    reviewed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username}'s application for {self.fund.name}"
