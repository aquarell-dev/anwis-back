from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import LeftOver


@admin.register(LeftOver)
class LeftOverAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'go_to_link', 'preview_image']
    list_display_links = ['id']

    def preview_image(self, obj):
        if obj:
            return mark_safe(f'<img src="{obj.photo_url}" width=50>')

    def go_to_link(self, obj):
        if obj:
            return mark_safe(f'<a href="{obj.url}" target="_blank">Перейти к товару</a>')

    preview_image.short_description = 'Картинка'
    go_to_link.short_description = 'Ссылка'
