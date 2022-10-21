from django.contrib import admin

from.models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.get_fields()]
    list_display_links = ['id']
    search_fields = ['id', 'status']


@admin.register(ChinaDistributor)
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChinaDistributor._meta.get_fields()]
    list_display_links = ['id']
    search_fields = ['id', 'china_distributor']


@admin.register(OrderForProject)
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderForProject._meta.get_fields()]
    list_display_links = ['id']
    search_fields = ['id', 'order_for_project']


@admin.register(IndividualEntrepreneur)
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IndividualEntrepreneur._meta.get_fields()]
    list_display_links = ['id']
    search_fields = ['id', 'individual_entrepreneur']


@admin.register(Order)
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.get_fields()]
    list_display_links = ['id']
    search_fields = ['id']
    list_filter = ['draft']
