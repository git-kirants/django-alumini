from django import forms
from .models import JobPosting, JobApplication

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'company', 'company_logo', 'location', 'job_type', 'description', 'requirements', 'benefits', 'deadline']
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
            })
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status', 'notes'] 