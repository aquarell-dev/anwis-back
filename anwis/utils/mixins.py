from django.utils.safestring import mark_safe


class ImagePreviewMixin:
    def preview_image(self, obj):
        if obj and obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')
        else:
            return mark_safe(f'<p>No photo</p>')

    preview_image.short_description = 'Картинка'
