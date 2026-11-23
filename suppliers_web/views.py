"""Список, карточки и формы поставщиков."""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import SupplierFilterForm, SupplierForm
from .models import Supplier
from orm_utils import casefold_exact_search, casefold_search


def suppliers(request):
    form = SupplierFilterForm(request.GET or None)
    items = Supplier.objects.all()
    if form.is_valid():
        data = form.cleaned_data
        if data.get("exact_name"):
            items = casefold_exact_search(items, "name", data["exact_name"])
        if data.get("q"):
            items = casefold_search(items, data["q"], ["name", "contact"])
        if data.get("min_rating") is not None:
            items = items.filter(rating__gte=data["min_rating"])
    items = items.order_by("-rating", "name")
    page_obj = Paginator(items, 6).get_page(request.GET.get("page"))
    return render(request, "suppliers/supplier_list.html", {
        "suppliers": page_obj, "page_obj": page_obj, "filter_form": form,
    })


def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    return render(request, "suppliers/supplier_detail.html", {"supplier": supplier})


@require_http_methods(["GET", "POST"])
def supplier_create(request):
    form = SupplierForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        supplier = form.save()
        return redirect("suppliers:detail", supplier_id=supplier.pk)
    return render(request, "suppliers/supplier_form.html", {"form": form, "is_create": True})


@require_http_methods(["GET", "POST"])
def supplier_update(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    form = SupplierForm(request.POST or None, instance=supplier)
    if request.method == "POST" and form.is_valid():
        supplier = form.save()
        return redirect("suppliers:detail", supplier_id=supplier.pk)
    return render(request, "suppliers/supplier_form.html", {"form": form, "supplier": supplier})
