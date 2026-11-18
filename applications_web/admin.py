from django.contrib import admin
from .models import Application, ApplicationItem


class ApplicationItemInline(admin.TabularInline):
    model = ApplicationItem
    extra = 1


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "purpose", "status")
    search_fields = ("id", "purpose")
    list_filter = ("status",)
    inlines = (ApplicationItemInline,)
