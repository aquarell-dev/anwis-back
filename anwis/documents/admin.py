from django.contrib import admin

from documents.models import Photo, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id']
