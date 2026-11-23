"""Маршруты каталога товаров."""
from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.products, name="list"),
    path("create/", views.product_create, name="create"),
    path("<str:product_id>/edit/", views.product_update, name="update"),
    path("slug/<slug:slug>/", views.product_detail_by_slug, name="detail-by-slug"),
    path("<str:product_id>/", views.product_detail, name="detail"),
]
