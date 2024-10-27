from django import forms
 
from .models import NewPost

class PostForm(forms.ModelForm):
    class Meta:
        model = NewPost
        fields = ['text']