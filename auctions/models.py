from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category= models.CharField(max_length=23, null=True)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    user = models.ForeignKey(User, null=True,  on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, null=True)
    price = models.FloatField(default=0.0)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    category= models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    is_closed= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.category})"

class Bid(models.Model):
    user = models.ForeignKey(User, null=True,  on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE, related_name="command")
    bid = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.listing} (${self.bid}) by {self.user}"

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, blank=True, on_delete=models.CASCADE, related_name='comment', null=True)
    comment = models.CharField(max_length=3003, null=True)

    def __str__(self):
        return f" {self.user} says {self.comment} on {self.listing}"  

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, blank=True , on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.user} add {self.listing} to his/her watchlist"
