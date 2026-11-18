"""Каталог товаров и карточки с использованием Django ORM."""
from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Product
from orm_utils import casefold_search


def products(request):
    query = request.GET.get("q", "").strip()[:100]
    min_price = request.GET.get("min_price", "").strip()
    items = Product.objects.all()
    error = None
    if query:
        items = casefold_search(items, query, ["name", "description"])
    if min_price:
        try:
            price_value = Decimal(min_price)
            if price_value < 0:
                raise InvalidOperation
            items = items.filter(price__gte=price_value)
        except (InvalidOperation, ValueError):
            error = "Укажите корректную неотрицательную цену."
            min_price = ""
    sort_fields = {"name": "name", "price": "price", "-price": "-price"}
    sort = request.GET.get("sort", "name")
    items = items.order_by(sort_fields.get(sort, "name"), "id")
    page_obj = Paginator(items, 6).get_page(request.GET.get("page"))
    return render(request, "products/product_list.html", {
        "products": page_obj, "page_obj": page_obj, "min_price": min_price,
        "query": query, "sort": sort, "error": error,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/product_detail.html", {"product": product})
