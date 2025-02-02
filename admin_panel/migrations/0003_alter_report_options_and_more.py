# Generated by Django 5.1.5 on 2025-01-21 04:49

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_report'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='report',
            old_name='generated_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='systemmetric',
            name='metric_type',
        ),
        migrations.AddField(
            model_name='systemmetric',
            name='metric_name',
            field=models.CharField(choices=[('system_load', 'System Load'), ('memory_usage', 'Memory Usage'), ('cpu_usage', 'CPU Usage'), ('disk_usage', 'Disk Usage'), ('network_traffic', 'Network Traffic'), ('db_query_rate', 'Database Query Rate'), ('cache_hit_rate', 'Cache Hit Rate'), ('error_rate', 'Error Rate'), ('avg_response_time', 'Average Response Time'), ('total_users', 'Total Users'), ('active_users', 'Active Users'), ('new_users', 'New Users'), ('engagement_rate', 'Engagement Rate')], default='system_load', max_length=50),
        ),
        migrations.AlterField(
            model_name='report',
            name='generated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='report_type',
            field=models.CharField(choices=[('user_activity', 'User Activity'), ('event_stats', 'Event Statistics'), ('donation_stats', 'Donation Statistics'), ('job_stats', 'Job Statistics'), ('system_metrics', 'System Metrics')], max_length=50),
        ),
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='systemmetric',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddIndex(
            model_name='systemmetric',
            index=models.Index(fields=['metric_name', '-timestamp'], name='admin_panel_metric__8b846d_idx'),
        ),
    ]
