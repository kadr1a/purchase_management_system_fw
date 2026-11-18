"""Представления раздела поставщиков."""
from django.shortcuts import render

from web_utils import get_project_data


def suppliers(request):
    """Передаёт список поставщиков в шаблон."""
    context = {"suppliers": get_project_data()["suppliers"]}
    return render(request, "suppliers/supplier_list.html", context)


def supplier_detail(request, supplier_id):
    """Передаёт поставщика или None в шаблон подробной страницы."""
    items = get_project_data()["suppliers"]
    supplier = next((item for item in items if item.id == supplier_id), None)
    return render(
        request,
        "suppliers/supplier_detail.html",
        {"supplier": supplier},
        status=404 if supplier is None else 200,
    )
