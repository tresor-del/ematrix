from django import forms 
from .models import Listing, Bid, Comment


class ListingForm(forms.ModelForm):
     
    class Meta:
        model = Listing
        fields = ["title", "slug", "price","description", "category", "image"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide url for your Listing. '}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Set the starting bid for the Listing'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': ''}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
            
        
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields= ["comment"]
        widgets={
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Comment this Listing here', 'style':'height: 50px;'})
        }

class BidForm(forms.ModelForm):

    class Meta:
        model= Bid
        fields=["bid"]
        widgets={
            "bid": forms.NumberInput(attrs={'class': 'form-control','placeholder':'Bid'})
        }


