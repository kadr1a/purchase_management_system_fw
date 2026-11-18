"""Маршруты поставщиков."""
from django.urls import path

from . import views

app_name = "suppliers"
urlpatterns = [
    path("", views.suppliers, name="list"),
    path("<str:supplier_id>/", views.supplier_detail, name="detail"),
]
