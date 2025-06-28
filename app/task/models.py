from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    profile_image = models.ImageField( upload_to='images/', default='images/profile_image.png', null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  
        blank=True,
        help_text='Les groupes auxquels cet utilisateur appartient.',
        verbose_name='groupes'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  
        blank=True,
        help_text='Les permissions spécifiques à cet utilisateur.',
        verbose_name='permissions utilisateur'
    )

    def __str__(self):
        return self.username

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


class Priority(models.TextChoices):
        
        IU = 'important and urgent' ,'Important and Urgent'
        InU = 'important but not urgent', 'Important but not Urgent'
        nIU = 'not important but urgent', 'Not important but Urgent'
        nInU = 'not important and not urgent', 'Not important and not Urgent'


class Task(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    due_date= models.DateField(auto_now=True, null=True, blank=True)
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


    def __str__(self):
         return self.title

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
