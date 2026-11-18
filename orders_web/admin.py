from django.contrib import admin
from .models import PurchaseOrder


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "supplier", "total", "status")
    search_fields = ("id", "application__purpose", "supplier__name")
    list_filter = ("status",)
