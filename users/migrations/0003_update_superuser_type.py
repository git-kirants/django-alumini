from django.db import migrations

def update_superuser_type(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.filter(is_superuser=True).update(user_type='admin')

def reverse_superuser_type(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.filter(is_superuser=True, user_type='admin').update(user_type='student')

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_company_user_current_company_and_more'),
    ]

    operations = [
        migrations.RunPython(update_superuser_type, reverse_superuser_type),
    ] 