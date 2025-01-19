from django import forms
from .models import NotificationPreference

class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = ['events_updates', 'job_postings', 'forum_replies', 'email_notifications']
        widgets = {
            field: forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-blue-600'})
            for field in fields
        } 