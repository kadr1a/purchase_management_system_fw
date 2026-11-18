from django.urls import path
from . import views

urlpatterns = [
    path("", views.orders, name="orders"),
    path("<str:order_id>/", views.order_detail, name="order_detail"),
]
