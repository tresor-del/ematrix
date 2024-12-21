from django.contrib import admin

from .models import CustomUser, Task, Notification, Friends, Project, GroupTask, Comment, ProjectActivity
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('author','title', 'priority' )

admin.site.register(CustomUser)
admin.site.register(Task, TaskAdmin)
admin.site.register(Notification)
admin.site.register(Friends)
admin.site.register(Project)
admin.site.register(GroupTask)
admin.site.register(Comment)
admin.site.register(ProjectActivity)