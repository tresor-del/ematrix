# Generated by Django 5.1.1 on 2024-12-09 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_group_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='tasks',
        ),
    ]
