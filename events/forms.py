from django import forms
from .models import Event, EventRegistration
from datetime import datetime
from django.utils.html import strip_tags

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'block w-full text-white text-sm file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-gradient-to-r file:from-blue-600 file:to-emerald-600 file:text-white hover:file:from-blue-700 hover:file:to-emerald-700 file:transition-all file:duration-200 file:shadow-lg file:shadow-blue-600/20',
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'h-5 w-5 rounded bg-white/10 border-white/20 text-blue-600 focus:ring-blue-500 focus:ring-offset-slate-800 focus:ring-offset-2 transition-colors duration-200'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full pl-4 pr-4 py-3 rounded-xl bg-slate-700 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200 appearance-none',
                    'style': '''
                        background-image: url('data:image/svg+xml,%3csvg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20"%3e%3cpath stroke="%23ffffff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 8l4 4 4-4"/%3e%3c/svg%3e');
                        background-position: right 0.75rem center;
                        background-repeat: no-repeat;
                        background-size: 1.5em 1.5em;
                        padding-right: 2.5rem;
                    '''
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full pl-4 pr-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
                })

            # Clean help text
            if field.help_text:
                field.help_text = strip_tags(field.help_text)

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'date',
            'location', 'capacity', 'registration_deadline',
            'is_online', 'meeting_link', 'image'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': datetime.now().strftime('%Y-%m-%dT%H:%M')
            }),
            'registration_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': datetime.now().strftime('%Y-%m-%dT%H:%M')
            }),
            'description': forms.Textarea(attrs={'rows': 4}),
            'event_type': forms.Select(attrs={
                'class': 'w-full pl-4 pr-4 py-3 rounded-xl bg-slate-700 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200 appearance-none',
                'style': '''
                    background-image: url('data:image/svg+xml,%3csvg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20"%3e%3cpath stroke="%23ffffff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 8l4 4 4-4"/%3e%3c/svg%3e');
                    background-position: right 0.75rem center;
                    background-repeat: no-repeat;
                    background-size: 1.5em 1.5em;
                    padding-right: 2.5rem;
                '''
            }),
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-white text-sm file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-gradient-to-r file:from-blue-600 file:to-emerald-600 file:text-white hover:file:from-blue-700 hover:file:to-emerald-700 file:transition-all file:duration-200 file:shadow-lg file:shadow-blue-600/20',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        registration_deadline = cleaned_data.get('registration_deadline')
        is_online = cleaned_data.get('is_online')
        meeting_link = cleaned_data.get('meeting_link')

        if date and registration_deadline and registration_deadline > date:
            raise forms.ValidationError(
                "Registration deadline cannot be after the event date."
            )
        
        if is_online and not meeting_link:
            self.add_error('meeting_link', 'Meeting link is required for online events.')
        elif not is_online:
            cleaned_data['meeting_link'] = ''

        return cleaned_data