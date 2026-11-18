"""Маршруты каталога товаров."""
from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.products, name="list"),
    path("<str:product_id>/", views.product_detail, name="detail"),
]
