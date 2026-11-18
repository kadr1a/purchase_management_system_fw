"""Список заявок и состав заявок через ORM."""
from decimal import Decimal

from django.core.paginator import Paginator
from django.db.models import Count, F, Sum, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render

from .models import Application, ApplicationItem
from orm_utils import casefold_search


def applications(request):
    query = request.GET.get("q", "").strip()[:100]
    status = request.GET.get("status", "").strip()
    exclude_status = request.GET.get("exclude_status", "").strip()
    sort_options = {"id": "id", "purpose": "purpose", "status": "status"}
    sort = request.GET.get("sort", "id")
    items = Application.objects.all().prefetch_related("items__product")
    if query:
        items = casefold_search(items, query, ["id", "purpose"])
    valid_statuses = ["Черновик", "Согласована", "Отклонена"]
    if status in valid_statuses:
        items = items.filter(status=status)
    elif status:
        status = ""
    if exclude_status in ["Черновик", "Согласована", "Отклонена"]:
        items = items.exclude(status=exclude_status)
    else:
        exclude_status = ""
    line_total = ExpressionWrapper(
        F("items__product__price") * F("items__quantity"),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )
    items = items.annotate(
        item_count=Count("items", distinct=True),
        application_total=Coalesce(Sum(line_total), Decimal("0.00")),
    ).order_by(sort_options.get(sort, "id"), "id")
    page_obj = Paginator(items, 5).get_page(request.GET.get("page"))
    return render(request, "applications/application_list.html", {
        "applications": page_obj, "page_obj": page_obj,
        "query": query, "status": status, "exclude_status": exclude_status,
        "sort": sort,
    })


def application_detail(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    items = (
        ApplicationItem.objects.filter(application=application)
        .select_related("product")
        .annotate(
            name=F("product__name"),
            price=F("product__price"),
            line_total=ExpressionWrapper(
                F("product__price") * F("quantity"),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            ),
        ).values("id", "name", "price", "quantity", "line_total")
        .order_by("name")
    )
    return render(request, "applications/application_detail.html", {
        "application": application, "items": items,
    })
