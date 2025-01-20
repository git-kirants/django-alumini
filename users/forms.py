from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow only 'alumni' and 'student' as user types
        choices = [(ut[0], ut[1]) for ut in User.USER_TYPES if ut[0] in ['alumni', 'student']]
        self.fields['user_type'].widget = forms.RadioSelect(choices=choices)

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Tell us about yourself...',
        }),
        required=False
    )
    
    skills = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Enter skills separated by commas',
        }),
        required=False
    )
    
    certifications = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Enter certifications separated by commas',
        }),
        required=False
    )
    
    achievements = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Enter your notable achievements and projects',
        }),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            'email',
            'graduation_year',
            'current_company',
            'current_job_title',
            'years_of_experience',
            'industry',
            'portfolio_link',
            'skills',
            'certifications',
            'achievements',
            'bio'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'graduation_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY'
            }),
            'current_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your current company'
            }),
            'current_job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your job title'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience'
            }),
            'industry': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your industry'
            }),
            'portfolio_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your portfolio URL'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')

        # Handle user type specific fields
        if user:
            if user.user_type == 'student':
                # Hide professional fields for students
                professional_fields = [
                    'current_company',
                    'current_job_title',
                    'years_of_experience',
                    'industry',
                    'portfolio_link',
                    'skills',
                    'certifications',
                    'achievements'
                ]
                for field in professional_fields:
                    self.fields[field].widget = forms.HiddenInput()
                    self.fields[field].required = False
            
            elif user.user_type == 'alumni':
                # Make certain fields required for alumni
                required_fields = [
                    'current_company',
                    'current_job_title',
                    'industry',
                    'years_of_experience'
                ]
                for field in required_fields:
                    self.fields[field].required = True

        # Add labels and help texts
        labels = {
            'bio': 'About Me',
            'portfolio_link': 'Portfolio Website',
            'years_of_experience': 'Years of Experience',
            'current_job_title': 'Job Title',
        }

        help_texts = {
            'profile_picture': 'Upload a profile picture (JPG, PNG)',
            'graduation_year': 'Enter your graduation year',
            'portfolio_link': 'Enter the URL to your portfolio website',
            'skills': 'List your key skills, separated by commas',
            'certifications': 'List your certifications, separated by commas',
            'achievements': 'Describe your notable achievements and projects'
        }

        # Apply labels and help texts
        for field_name, label in labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label

        for field_name, help_text in help_texts.items():
            if field_name in self.fields:
                self.fields[field_name].help_text = help_text

class StudentRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class AlumniRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
