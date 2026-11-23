"""Каталог товаров, фильтрация и операции создания/редактирования."""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ProductFilterForm, ProductForm
from .models import Product
from orm_utils import casefold_search


def products(request):
    form = ProductFilterForm(request.GET or None)
    items = Product.objects.all()
    if form.is_valid():
        data = form.cleaned_data
        if data.get("q"):
            items = casefold_search(items, data["q"], ["name", "description"])
        if data.get("min_price") is not None:
            items = items.filter(price__gte=data["min_price"])
        sort = data.get("sort") or "name"
    else:
        sort = "name"
    sort_field = {"name": "name", "price": "price", "-price": "-price"}.get(sort, "name")
    items = items.order_by(sort_field, "id")
    page_obj = Paginator(items, 6).get_page(request.GET.get("page"))
    return render(request, "products/product_list.html", {
        "products": page_obj, "page_obj": page_obj, "filter_form": form,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/product_detail.html", {"product": product})


def product_detail_by_slug(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "products/product_detail.html", {"product": product})


@require_http_methods(["GET", "POST"])
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        product = form.save()
        return redirect(product.get_absolute_url())
    return render(request, "products/product_form.html", {"form": form, "is_create": True})


@require_http_methods(["GET", "POST"])
def product_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        return redirect(form.save().get_absolute_url())
    return render(request, "products/product_form.html", {"form": form, "product": product})
