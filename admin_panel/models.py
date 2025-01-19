from django.db import models
from django.utils import timezone

class AdminReport(models.Model):
    REPORT_TYPES = (
        ('user_activity', 'User Activity'),
        ('event_stats', 'Event Statistics'),
        ('donation_summary', 'Donation Summary'),
        ('job_stats', 'Job Statistics'),
        ('system_metrics', 'System Metrics'),
    )

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    date_range_start = models.DateTimeField()
    date_range_end = models.DateTimeField()
    data = models.JSONField()
    
    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} - {self.generated_at.strftime('%Y-%m-%d')}"

class SystemMetric(models.Model):
    METRIC_TYPES = (
        ('user_count', 'Total Users'),
        ('active_users', 'Active Users'),
        ('event_count', 'Total Events'),
        ('donation_amount', 'Total Donations'),
        ('job_count', 'Total Jobs'),
        ('response_time', 'Average Response Time'),
    )

    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value}"
