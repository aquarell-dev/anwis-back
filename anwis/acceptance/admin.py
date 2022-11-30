from django.contrib import admin

from acceptance.models import Acceptance, StaffMember, Product, AcceptanceCategory, Box, AcceptanceStatus
from utils.mixins import PreviewColorMixin


@admin.register(Acceptance)
class AcceptanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Acceptance._meta.get_fields() if
                    field.name not in ['productsquantity', 'specifications', 'order', 'tasks', 'documents']]
    list_display_links = ['id']


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in StaffMember._meta.get_fields()
    ]
    list_display_links = ['id']


@admin.register(AcceptanceCategory)
class AcceptanceCategoryAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in AcceptanceCategory._meta.get_fields()
        if field.name not in ['product']
    ]
    list_display_links = ['id']


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Box._meta.get_fields()
        if field.name not in ['productspecification']
    ]
    list_display_links = ['id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'title']
    list_display_links = ['id']


@admin.register(AcceptanceStatus)
class StatusAdmin(PreviewColorMixin, admin.ModelAdmin):
    list_display = ['id', 'status', 'color', 'preview_color']
    list_display_links = ['id']
