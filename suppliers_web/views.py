"""Представления раздела поставщиков, работающие с SQLite."""

from django.shortcuts import render

from db.repository import SUPPLIER_LIST_SQL, fetch_all, fetch_one


def suppliers(request):
    """Показывает поставщиков и фильтрует их по минимальному рейтингу."""
    min_rating = request.GET.get("min_rating", "").strip()
    if min_rating:
        try:
            items = fetch_all(
                "SELECT id, name, contact, rating FROM suppliers "
                "WHERE rating >= ? ORDER BY rating DESC, name",
                (int(min_rating),),
            )
        except ValueError:
            items = fetch_all(SUPPLIER_LIST_SQL)
            min_rating = ""
    else:
        items = fetch_all(SUPPLIER_LIST_SQL)
    return render(
        request,
        "suppliers/supplier_list.html",
        {"suppliers": items, "min_rating": min_rating},
    )


def supplier_detail(request, supplier_id):
    """Передаёт поставщика из SQLite в шаблон подробной страницы."""
    supplier = fetch_one(
        "SELECT id, name, contact, rating FROM suppliers WHERE id = ?",
        (supplier_id,),
    )
    return render(
        request,
        "suppliers/supplier_detail.html",
        {"supplier": supplier},
        status=404 if supplier is None else 200,
    )
