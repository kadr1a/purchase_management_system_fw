"""Корневая маршрутизация веб-приложения."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("products/", include("products_web.urls")),
    path("suppliers/", include("suppliers_web.urls")),
    path("applications/", include("applications_web.urls")),
    path("orders/", include("orders_web.urls")),
]

if settings.DEBUG_TOOLBAR_ENABLED:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

admin.site.site_header = "Система управления закупками"
admin.site.site_title = "Администрирование закупок"
admin.site.index_title = "Управление данными системы"

handler404 = "homepage.views.page_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
