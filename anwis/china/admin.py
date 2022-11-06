from django.contrib import admin
from django.utils.safestring import mark_safe

from utils.mixins import ImagePreviewMixin
from .models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur, ProductQuantity, \
    Category, Task


@admin.register(Status)
class StatusAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['id', 'status', 'preview_color', 'preview_image']
    list_display_links = ['id']
    search_fields = ['id', 'status']

    def preview_color(self, obj):
        if obj:
            return mark_safe(
                f'<div style="display: flex; align-items:center;">'
                f'<div style="background-color: {obj.color}; width: 50px; height: 50px; border-radius: 50%;"></div>'
                f'<div style="margin-left:10px; background-color: {obj.hover_color}; width: 50px; height: 50px; '
                f'border-radius: 50%;">'
                f'</div>'
                '</div>'
            )

    preview_color.short_description = 'Превью цвета'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'datetime']
    list_display_links = ['id']


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
    list_display = ['id', 'title', 'article', 'preview_image', 'color', 'size', 'brand', 'category']
    list_display_links = ['id']


@admin.register(ProductQuantity)
class ProductQuantityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductQuantity._meta.get_fields() if field.name not in ['order']]
    list_display_links = ['id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.get_fields() if field.name not in ['order', 'product']]
    list_display_links = ['id']
