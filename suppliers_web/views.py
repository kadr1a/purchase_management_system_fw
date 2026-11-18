"""Список и карточка поставщика на Django ORM."""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Supplier
from orm_utils import casefold_exact_search, casefold_search


def suppliers(request):
    query = request.GET.get("q", "").strip()[:100]
    min_rating = request.GET.get("min_rating", "").strip()
    exact_name = request.GET.get("exact_name", "").strip()[:100]
    items = Supplier.objects.all()
    if exact_name:
        items = casefold_exact_search(items, "name", exact_name)
    error = None
    if query:
        items = casefold_search(items, query, ["name", "contact"])
    if min_rating:
        try:
            rating = int(min_rating)
            if rating not in range(1, 6):
                raise ValueError
            items = items.filter(rating__gte=rating)
        except ValueError:
            error = "Рейтинг должен быть целым числом от 1 до 5."
            min_rating = ""
    items = items.order_by("-rating", "name")
    page_obj = Paginator(items, 6).get_page(request.GET.get("page"))
    return render(request, "suppliers/supplier_list.html", {
        "suppliers": page_obj, "page_obj": page_obj,
        "min_rating": min_rating, "query": query,
        "exact_name": exact_name, "error": error,
    })


def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    return render(request, "suppliers/supplier_detail.html", {"supplier": supplier})
