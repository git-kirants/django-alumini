from django import forms
from .models import Message, MessageReport

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type your message...',
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200'
            })
        }

class MessageReportForm(forms.ModelForm):
    class Meta:
        model = MessageReport
        fields = ['reason', 'details']
        widgets = {
            'details': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Please provide additional details about your report...'
            })
        } 