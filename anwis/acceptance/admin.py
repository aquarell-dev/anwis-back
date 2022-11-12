from django.contrib import admin

from acceptance.models import Acceptance


@admin.register(Acceptance)
class AcceptanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Acceptance._meta.get_fields() if
                    field.name not in ['productsquantity', 'products']]
    list_display_links = ['id']
