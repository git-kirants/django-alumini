from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].widget = forms.RadioSelect(choices=User.USER_TYPES)

class ProfileUpdateForm(forms.ModelForm):
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter skills separated by commas",
        required=False
    )
    
    certifications = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter certifications separated by commas",
        required=False
    )
    
    achievements = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter your notable achievements and projects",
        required=False
    )

    class Meta:
        model = User
        fields = [
            'profile_picture', 
            'bio',
            'graduation_year',
            'current_job_title',
            'current_company',
            'industry',
            'years_of_experience',
            'skills',
            'achievements',
            'certifications',
            'linkedin_profile',
            'portfolio_link',
            'mentorship_availability',
            'first_name',
            'last_name',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')
        
        if user and user.user_type == 'admin':
            # For admin, only show basic fields
            admin_fields = ['username', 'email', 'password']
            for field in self.fields:
                if field not in admin_fields:
                    self.fields[field].widget = forms.HiddenInput()
                    self.fields[field].required = False
        elif user and user.user_type == 'alumni':
            required_fields = [
                'current_job_title',
                'current_company',
                'industry',
                'years_of_experience',
                'skills',
                'mentorship_availability'
            ]
            for field in required_fields:
                self.fields[field].required = True
        else:
            # For students, hide professional fields
            professional_fields = [
                'current_job_title',
                'current_company',
                'industry',
                'years_of_experience',
                'skills',
                'mentorship_availability'
            ]
            for field in professional_fields:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].required = False

        # Add Bootstrap classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
