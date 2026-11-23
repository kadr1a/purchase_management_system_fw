from django.contrib import admin
from django.db.models import Count

from .models import Application, ApplicationItem


class ApplicationItemInline(admin.TabularInline):
    model = ApplicationItem
    fields = ("product", "quantity", "unit_price", "line_total")
    readonly_fields = ("line_total",)
    autocomplete_fields = ("product",)
    extra = 1


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "purpose", "status", "items_count")
    list_display_links = ("id", "purpose")
    list_editable = ("status",)
    search_fields = ("id", "purpose", "items__product__name")
    list_filter = ("status",)
    ordering = ("id",)
    list_per_page = 25
    inlines = (ApplicationItemInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_items_count=Count("items"))

    @admin.display(description="Позиций", ordering="_items_count")
    def items_count(self, obj):
        return obj._items_count


@admin.register(ApplicationItem)
class ApplicationItemAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "product", "quantity", "unit_price", "line_total")
    list_display_links = ("id",)
    list_editable = ("quantity",)
    search_fields = ("application__id", "application__purpose", "product__name")
    list_filter = ("application__status",)
    ordering = ("application_id", "id")
    list_select_related = ("application", "product")
    autocomplete_fields = ("application", "product")
    list_per_page = 25
    readonly_fields = ("line_total",)
