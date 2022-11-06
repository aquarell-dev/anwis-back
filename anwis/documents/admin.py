from django.contrib import admin

from documents.models import Photo, Document
from utils.mixins import ImagePreviewMixin


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id']


@admin.register(Photo)
class PhotoAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['id', 'title', 'preview_image']
    list_display_links = ['id']
