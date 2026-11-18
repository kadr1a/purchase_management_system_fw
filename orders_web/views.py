"""Список и карточка заказов через Django ORM."""
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, render

from .models import PurchaseOrder
from orm_utils import casefold_search


def orders(request):
    query = request.GET.get("q", "").strip()[:100]
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "id")
    sort_fields = {
        "id": "id", "total": "total",
        "supplier": "supplier__name", "application": "application__purpose",
    }
    items = PurchaseOrder.objects.all()
    if query:
        items = casefold_search(
            items, query, ["id", "application__purpose", "supplier__name"],
        )
    if status in ["Оформлен", "Отменён"]:
        items = items.filter(status=status)
    elif status:
        status = ""
    items = items.annotate(
        purpose=F("application__purpose"),
        supplier_name=F("supplier__name"),
    ).values(
        "id", "total", "status", "application_id", "purpose", "supplier_name",
    ).order_by(sort_fields.get(sort, "id"), "id")
    page_obj = Paginator(items, 5).get_page(request.GET.get("page"))
    return render(request, "orders/order_list.html", {
        "orders": page_obj, "page_obj": page_obj, "query": query,
        "status": status, "sort": sort,
    })


def order_detail(request, order_id):
    order = get_object_or_404(
        PurchaseOrder.objects.select_related("application", "supplier"),
        pk=order_id,
    )
    order.application_id_display = order.application_id
    order.purpose = order.application.purpose
    order.supplier_name = order.supplier.name
    order.contact = order.supplier.contact
    return render(request, "orders/order_detail.html", {"order": order})
