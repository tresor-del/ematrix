from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class NewPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    text = models.TextField(max_length=300, null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.author} post {self.text}'
    
    @property
    def total_likes(self):
        return self.likes.count()
    
    def serialize(self):
        return {

            "content": self.text,
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(NewPost, on_delete=models.CASCADE, related_name="likes")

    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    following = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.user} followed {self.following.all()}'