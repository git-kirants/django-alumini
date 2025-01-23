from django import forms
from django.utils.html import strip_tags
from success.forms import DarkThemeFormMixin
from .models import Fund, Donation, ScholarshipApplication

class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['name', 'description', 'target_amount', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'message', 'is_anonymous']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message of support'}),
        }

class ScholarshipApplicationForm(DarkThemeFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full pl-4 pr-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
            })

    class Meta:
        model = ScholarshipApplication
        fields = ['academic_year', 'gpa', 'financial_need', 'achievements']
        widgets = {
            'financial_need': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your financial need...'
            }),
            'achievements': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'List your achievements...'
            }),
        }

class ScholarshipReviewForm(DarkThemeFormMixin, forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        amount_awarded = cleaned_data.get('amount_awarded')
        
        if status == 'approved' and not amount_awarded:
            self.add_error('amount_awarded', 'Amount is required when approving the application')
        
        return cleaned_data

    class Meta:
        model = ScholarshipApplication
        fields = ['status', 'amount_awarded']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full pl-4 pr-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200'
            }),
            'amount_awarded': forms.NumberInput(attrs={
                'class': 'w-full pl-4 pr-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-white/30 focus:ring-4 focus:ring-white/10 transition-all duration-200',
                'placeholder': 'Enter amount to be awarded'
            })
        }