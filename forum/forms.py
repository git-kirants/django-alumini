from django import forms
from .models import Thread, Reply, Category

class DarkThemeFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply dark theme styles to all fields
        for field_name, field in self.fields.items():
            # Base classes for all fields
            base_classes = "w-full rounded-xl border-white/10 text-white placeholder-slate-400 focus:border-blue-500 focus:ring-blue-500 transition-colors duration-200 px-6 py-4"
            
            # Additional styling for specific field types
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': f"{base_classes} h-14 bg-slate-700/90 appearance-none cursor-pointer",
                    'style': """
                        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
                        background-position: right 0.75rem center;
                        background-repeat: no-repeat;
                        background-size: 1.5em 1.5em;
                        padding-right: 2.5rem;
                    """
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{base_classes} bg-white/5 resize-none",
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': "block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-white/10 file:text-white hover:file:bg-white/20 transition-colors duration-200"
                })
            else:
                field.widget.attrs.update({
                    'class': f"{base_classes} bg-white/5"
                })

class ThreadForm(DarkThemeFormMixin, forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Thread title',
                'class': 'text-lg'
            }),
            'content': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Write your post here...',
                'class': 'text-lg'
            }),
        }

class ReplyForm(DarkThemeFormMixin, forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write your reply here...',
                'class': 'text-lg'
            }),
        }

class CategoryForm(DarkThemeFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Category name',
                'class': 'text-lg'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Category description',
                'class': 'text-lg'
            }),
        }