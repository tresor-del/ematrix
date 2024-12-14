# Generated by Django 5.1.1 on 2024-11-21 17:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_customuser_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('priority', models.CharField(choices=[('important and urgent', 'Important and Urgent'), ('important but not urgent', 'Important but not Urgent'), ('not important but ugent', 'Not important but Urgent'), ('not important and not urgent', 'Not important and not Urgent')], max_length=50)),
                ('category', models.CharField(blank=True, choices=[('study', 'Study'), ('work', 'Work'), ('private', 'Private'), ('family', 'Family'), ('job', 'Job'), ('health', 'Health'), ('finance', 'Finance'), ('leisure', 'Leisure'), ('travel', 'Travel'), ('other', 'Other')], max_length=50, null=True)),
                ('due_date', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
