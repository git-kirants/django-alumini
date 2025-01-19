# Generated by Django 5.1.5 on 2025-01-19 09:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('message', models.TextField(blank=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('donation_date', models.DateTimeField(auto_now_add=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to=settings.AUTH_USER_MODEL)),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='charitable.fund')),
            ],
        ),
        migrations.CreateModel(
            name='ScholarshipApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.CharField(max_length=9)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=3)),
                ('financial_need', models.TextField()),
                ('achievements', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('amount_awarded', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('applied_date', models.DateTimeField(auto_now_add=True)),
                ('reviewed_date', models.DateTimeField(blank=True, null=True)),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='charitable.fund')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_applications', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scholarship_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
