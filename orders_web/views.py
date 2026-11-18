"""Представления раздела заказов поставщикам."""
from django.shortcuts import render

from web_utils import get_project_data


def orders(request):
    """Передаёт список заказов в шаблон."""
    context = {"orders": get_project_data()["orders"]}
    return render(request, "orders/order_list.html", context)


def order_detail(request, order_id):
    """Передаёт заказ или None в шаблон подробной страницы."""
    items = get_project_data()["orders"]
    order = next((item for item in items if item.id == order_id), None)
    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
        status=404 if order is None else 200,
    )
