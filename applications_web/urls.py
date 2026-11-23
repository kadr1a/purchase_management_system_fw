"""Маршруты заявок."""
from django.urls import path

from . import views

app_name = "applications"
urlpatterns = [
    path("", views.applications, name="list"),
    path("create/", views.application_create, name="create"),
    path("<str:application_id>/edit/", views.application_update, name="update"),
    path("<str:application_id>/", views.application_detail, name="detail"),
]
