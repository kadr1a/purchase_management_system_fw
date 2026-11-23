"""Список, карточка и оформление заказов через формы Django."""
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_http_methods

from applications_web.models import Application
from .forms import OrderFilterForm, PurchaseOrderForm
from .models import PurchaseOrder
from orm_utils import casefold_search


def orders(request):
    form = OrderFilterForm(request.GET or None)
    items = PurchaseOrder.objects.all()
    if form.is_valid():
        data = form.cleaned_data
        if data.get("q"):
            items = casefold_search(
                items, data["q"], ["id", "application__purpose", "supplier__name"],
            )
        if data.get("status"):
            items = items.filter(status=data["status"])
        sort = data.get("sort") or "id"
    else:
        sort = "id"
    sort_fields = {
        "id": "id", "total": "total", "supplier": "supplier__name",
        "application": "application__purpose",
    }
    items = items.annotate(
        purpose=F("application__purpose"), supplier_name=F("supplier__name"),
    ).values(
        "id", "total", "status", "application_id", "purpose", "supplier_name",
    ).order_by(sort_fields.get(sort, "id"), "id")
    page_obj = Paginator(items, 5).get_page(request.GET.get("page"))
    return render(request, "orders/order_list.html", {
        "orders": page_obj, "page_obj": page_obj, "filter_form": form,
    })


def order_detail(request, order_id):
    order = get_object_or_404(
        PurchaseOrder.objects.select_related("application", "supplier"), pk=order_id,
    )
    order.application_id_display = order.application_id
    order.purpose = order.application.purpose
    order.supplier_name = order.supplier.name
    order.contact = order.supplier.contact
    return render(request, "orders/order_detail.html", {"order": order})


@require_http_methods(["GET", "POST"])
def order_create(request):
    form = PurchaseOrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save(commit=False)
        application_summary = Application.objects.with_summary().get(pk=order.application_id)
        order.total = application_summary.application_total
        order.save()
        return redirect("orders:detail", order_id=order.pk)
    return render(request, "orders/order_form.html", {"form": form})


@require_POST
def order_cancel(request, order_id):
    order = get_object_or_404(PurchaseOrder.objects.ordered(), pk=order_id)
    order.cancel()
    return redirect("orders:detail", order_id=order.pk)
