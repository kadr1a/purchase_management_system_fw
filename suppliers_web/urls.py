"""Маршруты поставщиков."""
from django.urls import path

from . import views

app_name = "suppliers"
urlpatterns = [
    path("", views.suppliers, name="list"),
    path("create/", views.supplier_create, name="create"),
    path("<str:supplier_id>/edit/", views.supplier_update, name="update"),
    path("<str:supplier_id>/", views.supplier_detail, name="detail"),
]
