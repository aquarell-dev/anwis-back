from django.contrib import admin
from django.utils.safestring import mark_safe

from utils.mixins import ImagePreviewMixin, PreviewColorMixin
from .models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur, ProductInfo, \
    Category


@admin.register(Status)
class StatusAdmin(PreviewColorMixin, ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['id', 'status', 'preview_color', 'preview_image']
    list_display_links = ['id']
    search_fields = ['id', 'status']


@admin.register(ChinaDistributor)
class ChinaDistributorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChinaDistributor._meta.get_fields() if field.name not in ['order']]
    list_display_links = ['id']
    search_fields = ['id', 'china_distributor']


@admin.register(OrderForProject)
class OrderForProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderForProject._meta.get_fields() if field.name not in ['order']]
    list_display_links = ['id']
    search_fields = ['id', 'order_for_project']


@admin.register(IndividualEntrepreneur)
class IndividualEntrepreneurAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IndividualEntrepreneur._meta.get_fields() if field.name not in ['order']]
    list_display_links = ['id']
    search_fields = ['id', 'individual_entrepreneur']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'china_distributor', 'total_quantity', 'cargo_number', 'date', 'delivered', 'draft']
    list_display_links = ['id']
    search_fields = ['id']
    list_filter = ['draft', 'delivered']


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['id', 'title', 'preview_image', 'article', 'color', 'size', 'brand', 'category']
    list_display_links = ['id']

    def preview_image(self, obj):
        if obj and obj.photo:
            return mark_safe(f'<img src="{obj.photo.photo.url}" width=50>')
        else:
            return mark_safe(f'<p>No photo</p>')

    preview_image.short_description = 'Картинка'


@admin.register(ProductInfo)
class ProductQuantityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInfo._meta.get_fields() if field.name not in ['order']]
    list_display_links = ['id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.get_fields() if field.name not in ['order', 'product']]
    list_display_links = ['id']
