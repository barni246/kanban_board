from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','id', 'short_description','task_index', 'column', 'created_at','updated_at', 'created_by')

    def short_description(self, obj):
        if len(obj.description) > 20:
            return obj.description[:20] + ' . . .'
        else:
            return obj.description

admin.site.register(Task, TaskAdmin)
