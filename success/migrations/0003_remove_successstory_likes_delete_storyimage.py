# Generated by Django 5.1.5 on 2025-01-23 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('success', '0002_successstory_likes_storyimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='successstory',
            name='likes',
        ),
        migrations.DeleteModel(
            name='StoryImage',
        ),
    ]
