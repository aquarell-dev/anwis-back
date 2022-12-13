from django.contrib import admin

from common.models import Task, Project, IndividualEntrepreneur


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'datetime']
    list_display_links = ['id']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.get_fields() if field.name not in ['order', 'acceptance']]
    list_display_links = ['id']
    search_fields = ['id', 'project']


@admin.register(IndividualEntrepreneur)
class IndividualEntrepreneurAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IndividualEntrepreneur._meta.get_fields() if field.name not in ['order', 'acceptance']]
    list_display_links = ['id']
    search_fields = ['id', 'individual_entrepreneur']
