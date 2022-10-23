from django.utils.safestring import mark_safe


class ImagePreviewMixin:
    def preview_image(self, obj):
        if obj:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')

    preview_image.short_description = 'Картинка'
