from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    #bio = models.TextField(max_length=150, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Utiliser un nom unique ici
        blank=True,
        help_text='Les groupes auxquels cet utilisateur appartient.',
        verbose_name='groupes'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Utiliser un nom unique ici
        blank=True,
        help_text='Les permissions spécifiques à cet utilisateur.',
        verbose_name='permissions utilisateur'
    )

    def __str__(self):
        return self.username
    

## Task models

class Priority(models.TextChoices):
        
        IU = 'important and urgent' ,'Important and Urgent'
        InU = 'important but not urgent', 'Important but not Urgent'
        nIU = 'not important but ugent', 'Not important but Urgent'
        nInU = 'not important and not urgent', 'Not important and not Urgent'

class Category(models.TextChoices):
    STUDY = 'study', 'Study' 
    WORK = 'work', 'Work' 
    PRIVATE = 'private', 'Private' 
    FAMILY = 'family', 'Family' 
    JOB = 'job', 'Job' 
    HEALTH = 'health', 'Health' 
    FINANCE = 'finance', 'Finance' 
    LEISURE = 'leisure', 'Leisure' 
    TRAVEL = 'travel', 'Travel' 
    OTHER = 'other', 'Other'

class Task(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    due_date= models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
         max_length=50,
         choices=Priority.choices,
    )
    category = models.CharField(
         max_length=50,
         choices= Category.choices,
         null=True,
         blank=True
    )
    due_date = models.DateField()


    def __str__(self):
         return {self.title}

    def serialize(self):
         return {
              'id': self.id,
              'author': self.author,
              'title': self.title,
              'description': self.description,
              'created_at': self.created_at,
              'update_at': self.updated_at,
              'due_date': self.due_date,
              'completed': self.completed,
              'priority': self.priority,
              'category': self.category,
         }


    def remaining_days(self):
        now = timezone.now().date()
        remaining_time = self.due_date - now
        return remaining_time.days

    

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" Notification for {self.user.username} at {self.created_at}"


class Friends(models.Model):
    friends = models.ManyToManyField(CustomUser, related_name='collaborators')
    
    
    def __str__(self):
        return self.friends
     