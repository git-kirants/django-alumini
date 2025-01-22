from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.validators import EmailValidator
from django.utils.html import strip_tags

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
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full pl-12 pr-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
            })
            # Clean help text and format password requirements
            if field.help_text:
                help_text = strip_tags(field.help_text)
                if field_name in ['password1']:
                    # Split password requirements into bullet points
                    requirements = [
                        "Your password can't be too similar to your other personal information.",
                        "Your password must contain at least 8 characters.",
                        "Your password can't be a commonly used password.",
                        "Your password can't be entirely numeric."
                    ]
                    field.help_text = "• " + "\n• ".join(requirements)
                else:
                    field.help_text = help_text

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = 'student'  # Set user type as student
        if commit:
            user.save()
        return user

class AlumniRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    current_job_title = forms.CharField(required=True)
    current_company = forms.CharField(required=True)
    industry = forms.ChoiceField(
        choices=User.INDUSTRY_CHOICES,
        required=True
    )
    years_of_experience = forms.IntegerField(required=True)
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        help_text="Enter your skills separated by commas"
    )
    mentorship_availability = forms.ChoiceField(
        choices=User.AVAILABILITY_CHOICES,
        required=True,
        help_text="Select your availability for mentoring students"
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'current_job_title', 'current_company', 'industry',
            'years_of_experience', 'skills', 'mentorship_availability',
            'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full pl-12 pr-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
            })
            # Clean help text and format password requirements
            if field.help_text:
                help_text = strip_tags(field.help_text)
                if field_name in ['password1']:
                    # Split password requirements into bullet points
                    requirements = [
                        "Your password can't be too similar to your other personal information.",
                        "Your password must contain at least 8 characters.",
                        "Your password can't be a commonly used password.",
                        "Your password can't be entirely numeric."
                    ]
                    field.help_text = "• " + "\n• ".join(requirements)
                else:
                    field.help_text = help_text

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.current_job_title = self.cleaned_data['current_job_title']
        user.current_company = self.cleaned_data['current_company']
        user.industry = self.cleaned_data['industry']
        user.years_of_experience = self.cleaned_data['years_of_experience']
        user.skills = self.cleaned_data['skills']
        user.mentorship_availability = self.cleaned_data['mentorship_availability']
        user.user_type = 'alumni'
        
        if commit:
            user.save()
        return user