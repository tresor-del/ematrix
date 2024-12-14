from django import forms
from .models import Task, Project
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter task title',
                'aria-label': 'New Task',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter task description',
                'aria-label': 'Description',
                'style': 'height: 100px;',
                'required': True
            }),
            'due_date': forms.TextInput(attrs={
                'id': 'due_date',
                'class': 'form-control',
                'placeholder': 'select date',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-sm mb-3',
                'id': 'id_category',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select form-select-sm mb-3',
                'id': 'id_priority',
                'required': True
            }),
        }

        def clean(self):
            cleaned_data = super().clean()  
        
            for field in ['title', 'description', 'due_date', 'category', 'priority']:
                if not cleaned_data.get(field):
                    raise forms.ValidationError(f"{field.capitalize()} is required.")
            
            return cleaned_data
        

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'category', 'members']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter task title',
                'aria-label': 'New Task',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter task description',
                'aria-label': 'Description',
                'style': 'height: 100px;',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-sm mb-3',
                'id': 'id_category',
                'required': True
            }),
            'members': forms.Select(attrs={
                'class': 'form-select form-select-sm mb-3',
                'id': 'id_category',
                'required': True
            })
        }

        def __init__(self, *args, **kwargs):
            owner = kwargs.pop('owner')  # Expect the owner to be passed in as a keyword argument
            super().__init__(*args, **kwargs)
            # Restrict the members field to only the owner's friends
            if owner:
                self.fields['members'].queryset = owner.friends.get_friends()

