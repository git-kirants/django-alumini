from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.validators import EmailValidator

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
    email = forms.EmailField(
        validators=[EmailValidator()],
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark required fields
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if self.fields[field_name].label:  # Check if label exists
                    self.fields[field_name].label += " *"
                else:
                    self.fields[field_name].label = field_name.title() + " *"
        # Customize field labels and styling
        field_labels = {
            'username': "Username",
            'email': "Email Address",
            'first_name': "First Name",
            'last_name': "Last Name",
            'password1': "Password",
            'password2': "Confirm Password"
        }
        
        for field_name, field in self.fields.items():
            # Set labels
            field.label = field_labels.get(field_name, field.label)
            
            # Update widget attributes
            field.widget.attrs.update({
                'class': 'form-control w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
            })

            # Make help text white
            if field.help_text:
                field.help_text = f'<span class="text-white/70 text-sm">{field.help_text}</span>'

class AlumniRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        validators=[EmailValidator()],
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark required fields
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if self.fields[field_name].label:  # Check if label exists
                    self.fields[field_name].label += " *"
                else:
                    self.fields[field_name].label = field_name.title() + " *"
        # Customize field labels and styling
        field_labels = {
            'username': "Username",
            'email': "Email Address",
            'first_name': "First Name",
            'last_name': "Last Name",
            'password1': "Password",
            'password2': "Confirm Password"
        }
        
        for field_name, field in self.fields.items():
            # Set labels
            field.label = field_labels.get(field_name, field.label)
            
            # Update widget attributes
            field.widget.attrs.update({
                'class': 'form-control w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
            })

            # Make help text white
            if field.help_text:
                field.help_text = f'<span class="text-white/70 text-sm">{field.help_text}</span>'