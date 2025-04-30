from django.contrib import admin

from .models import CustomUser, Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('author','title', 'priority' )

admin.site.register(CustomUser)
admin.site.register(Task, TaskAdmin)