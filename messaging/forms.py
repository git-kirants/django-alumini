from django import forms
from .models import Message, MessageReport

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Type a message...'
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