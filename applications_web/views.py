"""Представления раздела заявок на закупку."""
from django.shortcuts import render

from web_utils import get_project_data


def applications(request):
    """Передаёт список заявок в шаблон."""
    context = {"applications": get_project_data()["applications"]}
    return render(request, "applications/application_list.html", context)


def application_detail(request, application_id):
    """Передаёт заявку или None в шаблон подробной страницы."""
    items = get_project_data()["applications"]
    application = next(
        (item for item in items if item.id == application_id), None
    )
    return render(
        request,
        "applications/application_detail.html",
        {"application": application},
        status=404 if application is None else 200,
    )
