from django.contrib import admin

from orders_web.models import PurchaseOrder
from .models import Supplier


class SupplierPurchaseOrderInline(admin.TabularInline):
    model = PurchaseOrder
    fields = ("id", "application", "total", "status")
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rating", "contact")
    list_display_links = ("id", "name")
    list_editable = ("rating",)
    search_fields = ("id", "name", "contact")
    list_filter = ("rating",)
    ordering = ("-rating", "name")
    list_per_page = 25
    inlines = (SupplierPurchaseOrderInline,)
