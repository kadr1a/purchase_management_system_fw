"""Представления каталога товаров, работающие с SQLite."""

from django.shortcuts import render

from db.repository import PRODUCT_LIST_SQL, PRODUCT_SEARCH_SQL, fetch_all, fetch_one


def products(request):
    """Показывает каталог и поддерживает поиск по минимальной цене."""
    min_price = request.GET.get("min_price", "").strip()
    if min_price:
        try:
            price_value = float(min_price)
            items = fetch_all(PRODUCT_SEARCH_SQL, (price_value,))
        except ValueError:
            items = fetch_all(PRODUCT_LIST_SQL)
            min_price = ""
    else:
        items = fetch_all(PRODUCT_LIST_SQL)
    return render(
        request,
        "products/product_list.html",
        {"products": items, "min_price": min_price},
    )


def product_detail(request, product_id):
    """Передаёт товар из SQLite в шаблон подробной страницы."""
    product = fetch_one(
        "SELECT id, name, price, description FROM products WHERE id = ?",
        (product_id,),
    )
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
        status=404 if product is None else 200,
    )
