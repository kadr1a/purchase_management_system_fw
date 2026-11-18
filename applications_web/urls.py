"""Маршруты заявок."""
from django.urls import path

from . import views

app_name = "applications"
urlpatterns = [
    path("", views.applications, name="list"),
    path("<str:application_id>/", views.application_detail, name="detail"),
]
