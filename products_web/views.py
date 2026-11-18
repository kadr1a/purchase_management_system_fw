"""Представления каталога товаров."""
from django.shortcuts import render

from web_utils import get_project_data


def products(request):
    """Передаёт список товаров в шаблон каталога."""
    context = {"products": get_project_data()["products"]}
    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    """Передаёт товар или None в шаблон подробной страницы."""
    items = get_project_data()["products"]
    product = next((item for item in items if item.id == product_id), None)
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
        status=404 if product is None else 200,
    )
