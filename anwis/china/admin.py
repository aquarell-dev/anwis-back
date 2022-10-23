from django.contrib import admin

from utils.mixins import ImagePreviewMixin
from.models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.get_fields() if field.name not in ['order']]
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
    list_display = [field.name for field in Order._meta.get_fields() if field.name not in ['products']]
    list_display_links = ['id']
    search_fields = ['id']
    list_filter = ['draft']


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.get_fields() if field.name not in ['order']] + [
        'preview_image'
    ]
    list_display_links = ['id']
