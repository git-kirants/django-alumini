from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

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
    METRIC_TYPES = [
        ('system_load', 'System Load'),
        ('memory_usage', 'Memory Usage'),
        ('cpu_usage', 'CPU Usage'),
        ('disk_usage', 'Disk Usage'),
        ('network_traffic', 'Network Traffic'),
        ('db_query_rate', 'Database Query Rate'),
        ('cache_hit_rate', 'Cache Hit Rate'),
        ('error_rate', 'Error Rate'),
        ('avg_response_time', 'Average Response Time'),
        ('total_users', 'Total Users'),
        ('active_users', 'Active Users'),
        ('new_users', 'New Users'),
        ('engagement_rate', 'Engagement Rate'),
    ]

    metric_name = models.CharField(
        max_length=50, 
        choices=METRIC_TYPES,
        default='system_load'
    )
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric_name', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.get_metric_name_display()} - {self.timestamp}"

class Report(models.Model):
    REPORT_TYPES = [
        ('user_activity', 'User Activity'),
        ('event_stats', 'Event Statistics'),
        ('donation_stats', 'Donation Statistics'),
        ('job_stats', 'Job Statistics'),
        ('system_metrics', 'System Metrics'),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()
    file_path = models.FileField(upload_to='reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('admin_panel:view_report', args=[str(self.id)])
