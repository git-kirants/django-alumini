from django import forms
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

class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = ['academic_year', 'gpa', 'financial_need', 'achievements']
        widgets = {
            'financial_need': forms.Textarea(attrs={'rows': 4}),
            'achievements': forms.Textarea(attrs={'rows': 4}),
        }

class ScholarshipReviewForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = ['status', 'amount_awarded'] 