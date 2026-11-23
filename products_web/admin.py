from django.contrib import admin

from applications_web.models import ApplicationItem
from .models import Product


class ProductApplicationItemInline(admin.TabularInline):
    model = ApplicationItem
    fk_name = "product"
    fields = ("application", "quantity", "unit_price", "line_total")
    readonly_fields = ("line_total",)
    autocomplete_fields = ("application",)
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "slug")
    list_display_links = ("id", "name")
    list_editable = ("price",)
    search_fields = ("id", "name", "description", "slug")
    list_filter = ("price",)
    ordering = ("name",)
    list_per_page = 25
    readonly_fields = ("slug",)
    view_on_site = True
    inlines = (ProductApplicationItemInline,)
