"""Представления заявок на закупку, использующие SQL-запросы."""

from django.shortcuts import render

from db.repository import APPLICATION_LIST_SQL, fetch_all, fetch_one


def applications(request):
    """Показывает заявки с количеством позиций и общей стоимостью."""
    items = fetch_all(APPLICATION_LIST_SQL)
    return render(
        request,
        "applications/application_list.html",
        {"applications": items},
    )


def application_detail(request, application_id):
    """Показывает заявку и связанные с ней товарные позиции."""
    application = fetch_one(
        "SELECT id, purpose, status FROM applications WHERE id = ?",
        (application_id,),
    )
    items = fetch_all(
        "SELECT p.id, p.name, p.price, ai.quantity, "
        "p.price * ai.quantity AS line_total "
        "FROM application_items AS ai "
        "JOIN products AS p ON p.id = ai.product_id "
        "WHERE ai.application_id = ? ORDER BY p.name",
        (application_id,),
    )
    return render(
        request,
        "applications/application_detail.html",
        {"application": application, "items": items},
        status=404 if application is None else 200,
    )
