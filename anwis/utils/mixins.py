from django.utils.safestring import mark_safe


class ImagePreviewMixin:
    def preview_image(self, obj):
        if obj and obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')
        else:
            return mark_safe(f'<p>No photo</p>')

    preview_image.short_description = 'Картинка'


class ListModelMixin:
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(ListModelMixin, self).get_serializer(*args, **kwargs)


class PreviewColorMixin:
    def preview_color(self, obj):
        preview_hover = False

        if hasattr(obj, 'hover_color'):
            preview_hover = True

        if obj:
            return mark_safe(
                f'<div style="display: flex; align-items:center;">'
                f'<div style="background-color: {obj.color}; width: 50px; height: 50px; border-radius: 50%;"></div>'
                f'<div style="margin-left:10px; background-color: {"white" if not preview_hover else obj.hover_color}; width: 50px; height: 50px; '
                f'border-radius: 50%;">'
                f'</div>'
                '</div>'
            )

    preview_color.short_description = 'Превью цвета'
