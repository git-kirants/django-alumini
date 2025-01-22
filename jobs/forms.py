from django import forms
from .models import JobPosting, JobApplication

class DarkThemeFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply dark theme styles to all fields
        for field_name, field in self.fields.items():
            # Base classes for all fields
            base_classes = "w-full rounded-xl border-white/10 text-white placeholder-slate-400 focus:border-blue-500 focus:ring-blue-500 transition-colors duration-200"
            
            # Additional styling for specific field types
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': f"{base_classes} h-12 bg-slate-700/90 px-4 py-2 appearance-none cursor-pointer",
                    'style': """
                        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
                        background-position: right 0.75rem center;
                        background-repeat: no-repeat;
                        background-size: 1.5em 1.5em;
                        padding-right: 2.5rem;
                    """
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{base_classes} bg-white/5 resize-none",
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': "block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-white/10 file:text-white hover:file:bg-white/20 transition-colors duration-200"
                })
            else:
                field.widget.attrs.update({
                    'class': f"{base_classes} bg-white/5"
                })

class JobPostingForm(DarkThemeFormMixin, forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'company', 'company_logo', 'location', 'job_type', 'experience_level', 'salary_range', 'description', 'requirements', 'benefits', 'deadline']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Enter a detailed job description...'
            }),
            'requirements': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter job requirements (one per line)...'
            }),
            'benefits': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter job benefits (one per line)...'
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date'
            }),
            'salary_range': forms.TextInput(attrs={
                'placeholder': 'e.g. $50,000 - $70,000 per year'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'min': '0',
                'max': '50',
                'placeholder': 'Enter required years of experience'
            })
        }

class JobApplicationForm(DarkThemeFormMixin, forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your cover letter here...'
            }),
        }
        help_texts = {
            'resume': 'Upload your resume (PDF format recommended)',
            'cover_letter': 'Introduce yourself and explain why you\'re a good fit for this position'
        }

class ApplicationStatusForm(DarkThemeFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add color indicators to status choices
        status_field = self.fields['status']
        original_choices = dict(status_field.choices)
        
        # Define color classes for each status
        status_colors = {
            'pending': '',
            'reviewing': '',
            'shortlisted': '',
            'interviewed': '',
            'offered': '',
            'accepted': '',
            'rejected': '',
            'withdrawn': ''
        }
        
        # Update choices with color indicators
        new_choices = [
            (key, f"{status_colors.get(key, '')} {value}")
            for key, value in original_choices.items()
        ]
        status_field.choices = new_choices

    class Meta:
        model = JobApplication
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add any notes about this application status change...'
            }),
            'status': forms.Select(attrs={
                'class': 'custom-dropdown',
                'style': 'background-color: #333; color: #fff; padding: 10px; border: 1px solid #555;'
            })
        }
        help_texts = {
            'status': 'Select the new status for this application',
            'notes': 'Optional: Add any relevant notes about this status change'
        }