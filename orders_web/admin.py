from django.contrib import admin, messages

from .models import PurchaseOrder


@admin.action(description="Отменить выбранные оформленные заказы")
def cancel_selected_orders(modeladmin, request, queryset):
    cancelled = 0
    for order in queryset.select_related("application", "supplier"):
        try:
            order.cancel()
        except ValueError:
            continue
        cancelled += 1
    modeladmin.message_user(
        request, f"Отменено заказов: {cancelled}.", messages.SUCCESS,
    )


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "supplier", "total", "status")
    list_display_links = ("id",)
    search_fields = ("id", "application__purpose", "supplier__name")
    list_filter = ("status", "supplier")
    ordering = ("id",)
    list_select_related = ("application", "supplier")
    autocomplete_fields = ("application", "supplier")
    list_per_page = 25
    actions = (cancel_selected_orders,)
