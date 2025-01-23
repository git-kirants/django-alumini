from django import forms
from .models import SuccessStory, Comment
from django.forms.widgets import TextInput, Textarea, Select, FileInput
from django.utils.safestring import mark_safe

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class DarkThemeFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply dark theme styles to all fields
        for field_name, field in self.fields.items():
            # Base classes for all fields
            base_classes = "w-full rounded-xl border-white/10 text-white placeholder-slate-400 focus:border-blue-500 focus:ring-blue-500 transition-colors duration-200"
            
            # Set label color to white with slight transparency
            field.label = mark_safe(f'<span class="text-white/90 font-medium mb-2">{field.label}</span>')
            
            # Set help text color to white with more transparency
            if field.help_text:
                field.help_text = mark_safe(f'<span class="text-slate-300 text-sm mt-1">{field.help_text}</span>')
            
            # Additional styling for specific field types
            if isinstance(field.widget, Select):
                field.widget.attrs.update({
                    'class': f"{base_classes} h-12 bg-slate-900/90 px-4 py-2 appearance-none cursor-pointer",
                    'style': """
                        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
                        background-position: right 0.75rem center;
                        background-repeat: no-repeat;
                        background-size: 1.5em 1.5em;
                        padding-right: 2.5rem;
                    """
                })
            elif isinstance(field.widget, Textarea):
                field.widget.attrs.update({
                    'class': f"{base_classes} bg-white/5 resize-none p-6",
                })
            elif isinstance(field.widget, (FileInput, MultipleFileInput)):
                field.widget.attrs.update({
                    'class': "block w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-white/10 file:text-white hover:file:bg-white/20 transition-colors duration-200"
                })
            else:
                field.widget.attrs.update({
                    'class': f"{base_classes} bg-white/5"
                })

class SuccessStoryForm(DarkThemeFormMixin, forms.ModelForm):
    images = MultipleFileField(
        required=False,
        help_text='You can select multiple images by holding Ctrl (Windows) or Command (Mac) while selecting files'
    )

    class Meta:
        model = SuccessStory
        fields = ['title', 'content', 'graduation_year', 'current_position', 'company', 'image', 'images']
        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'Enter the title of your success story...',
                'class': 'text-lg'
            }),
            'content': Textarea(attrs={
                'rows': 8,
                'placeholder': 'Share your journey, challenges overcome, and achievements...'
            }),
            'graduation_year': TextInput(attrs={
                'min': '1900',
                'max': '2100',
                'placeholder': 'Enter your graduation year',
                'type': 'number'
            }),
            'current_position': TextInput(attrs={
                'placeholder': 'What is your current role?'
            }),
            'company': TextInput(attrs={
                'placeholder': 'Where do you currently work?'
            }),
        }
        help_texts = {
            'image': 'Upload a photo related to your success story (optional)',
            'content': 'Share your journey, challenges, and achievements to inspire others'
        }
        labels = {
            'title': 'Story Title',
            'content': 'Your Success Story',
            'graduation_year': 'Graduation Year',
            'current_position': 'Current Position',
            'company': 'Company',
            'image': 'Story Image',
            'images': 'Additional Images',
            'additional_images': 'Select Additional Images'
        }

class CommentForm(DarkThemeFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={
                'rows': 3, 
                'placeholder': ' Share your thoughts and congratulate your fellow alumni...',
                'class': 'text-lg text-center ml-12'
            }),
        }
        labels = {
            'content': 'Your Comment'
        }

class StoryReviewForm(DarkThemeFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add color indicators to status choices
        status_field = self.fields['status']
        status_colors = {
            'pending': 'text-yellow-400',
            'approved': 'text-emerald-400',
            'rejected': 'text-rose-400'
        }

    class Meta:
        model = SuccessStory
        fields = ['status']
        widgets = {
            'status': Select(attrs={
                'class': 'status-select'
            })
        }
        labels = {
            'status': 'Story Status'
        }