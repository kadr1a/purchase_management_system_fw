"""Список заявок и состав заявок через ORM."""
from django.core.paginator import Paginator
from django.db.models import F
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
    valid_statuses = Application.Status.values
    if status in valid_statuses:
        items = items.filter(status=status)
    elif status:
        status = ""
    if exclude_status in ["Черновик", "Согласована", "Отклонена"]:
        items = items.exclude(status=exclude_status)
    else:
        exclude_status = ""
    items = items.with_summary().order_by(sort_options.get(sort, "id"), "id")
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
        .annotate(name=F("product__name"), price=F("unit_price"))
        .values("id", "name", "price", "quantity", "line_total")
        .order_by("name")
    )
    return render(request, "applications/application_detail.html", {
        "application": application, "items": items,
    })
