from django import forms
from .models import SuccessStory, Comment

class SuccessStoryForm(forms.ModelForm):
    class Meta:
        model = SuccessStory
        fields = ['title', 'content', 'graduation_year', 'current_position', 'company', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your thoughts...'}),
        }

class StoryReviewForm(forms.ModelForm):
    class Meta:
        model = SuccessStory
        fields = ['status'] 