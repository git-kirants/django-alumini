from django import forms
from .models import Event, EventRegistration

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'date', 
            'location', 'capacity', 'registration_deadline',
            'is_online', 'meeting_link', 'image'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        registration_deadline = cleaned_data.get('registration_deadline')
        
        if date and registration_deadline and registration_deadline > date:
            raise forms.ValidationError(
                "Registration deadline cannot be after the event date."
            )
        
        return cleaned_data 