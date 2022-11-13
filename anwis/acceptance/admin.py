from django.contrib import admin

from acceptance.models import Acceptance, StaffMember


@admin.register(Acceptance)
class AcceptanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Acceptance._meta.get_fields() if
                    field.name not in ['productsquantity', 'products', 'order']]
    list_display_links = ['id']


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in StaffMember._meta.get_fields()
        # if field.name not in []
    ]
    list_display_links = ['id']
