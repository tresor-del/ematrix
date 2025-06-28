from django import forms
from .models import Task, CustomUser
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter task title',
                'aria-label': 'New Task',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': '(Optional)',
                'aria-label': 'Description',
                'style': 'height: 100px;',
            })
        }

        def clean(self):
            cleaned_data = super().clean()  
        
            for field in ['title', 'description', 'due_date', 'category', 'priority']:
                if not cleaned_data.get(field):
                    raise forms.ValidationError(f"{field.capitalize()} is required.")
            
            return cleaned_data
        