from django import forms
from .models import Task, Project, GroupTask, Friends, CustomUser
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
        

class ProjectForm(forms.ModelForm):

    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),  
        widget=forms.SelectMultiple(attrs={
            'name': 'name',
            'class': 'form-select form-select-sm mb-3',
            'id': 'id_members',
        })
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'category', 'members']
        widgets = {
                'name': forms.TextInput(attrs={
                    'name': 'name',
                    'class': 'form-control mb-3',
                    'aria-label': 'New Task',
                    'required': True,
                    'autofocus':'autofocus'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter task description',
                'aria-label': 'Description',
                'style': 'height: 100px;',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-sm mb-3',
                'id': 'id_category',
            }),
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)  
        super().__init__(*args, **kwargs)
        if owner:
            self.fields['members'].queryset = CustomUser.objects.filter(
            id__in=Friends.objects.filter(user=owner).values_list('friends', flat=True)
        )


class GroupTaskForm(forms.ModelForm):
    class Meta:
        model = GroupTask
        fields = [ 'name', 'description', 'assigned_to', ]

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
            'assigned_to': forms.Select(attrs={
                'class': 'form-select form-select-sm mb-3',
                'id':'id_asigned_to',
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)  
        super().__init__(*args, **kwargs)
        if owner:
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(
            id__in=Friends.objects.filter(user=owner).values_list('friends', flat=True)
        )