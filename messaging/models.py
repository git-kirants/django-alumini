from django.db import models
from django.conf import settings
from django.db.models import Q

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_other_participant(self, user):
        return self.participants.exclude(id=user.id).first()

    @property
    def other_participant(self):
        """This will raise an error if called without proper context, but that's what we want"""
        if not hasattr(self, '_request_user'):
            raise ValueError("Request user not set on conversation")
        return self.get_other_participant(self._request_user)

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()

    class Meta:
        ordering = ['-updated_at']

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

class MessageReport(models.Model):
    REPORT_REASONS = (
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('harassment', 'Harassment'),
        ('other', 'Other'),
    )

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='resolved_reports'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
