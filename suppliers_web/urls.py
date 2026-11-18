from django.urls import path
from . import views

urlpatterns = [
    path("", views.suppliers, name="suppliers"),
    path("<str:supplier_id>/", views.supplier_detail, name="supplier_detail"),
]
