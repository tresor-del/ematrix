# Generated by Django 5.1.1 on 2024-12-09 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_tag_alter_group_admins_alter_group_members_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='tasks',
            field=models.ManyToManyField(related_name='tasks', to='task.task'),
        ),
    ]
