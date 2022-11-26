from django.contrib import admin

from common.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'datetime']
    list_display_links = ['id']
