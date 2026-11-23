"""Список, карточка, создание и редактирование заявок."""
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ApplicationFilterForm, ApplicationForm, ApplicationItemFormSet
from .models import Application, ApplicationItem
from orm_utils import casefold_search


def applications(request):
    form = ApplicationFilterForm(request.GET or None)
    items = Application.objects.all().prefetch_related("items__product")
    if form.is_valid():
        data = form.cleaned_data
        if data.get("q"):
            items = casefold_search(items, data["q"], ["id", "purpose"])
        if data.get("status"):
            items = items.filter(status=data["status"])
        if data.get("exclude_status"):
            items = items.exclude(status=data["exclude_status"])
        sort = data.get("sort") or "id"
    else:
        sort = "id"
    ordering = {"id": "id", "purpose": "purpose", "status": "status"}.get(sort, "id")
    items = items.with_summary().order_by(ordering, "id")
    page_obj = Paginator(items, 5).get_page(request.GET.get("page"))
    return render(request, "applications/application_list.html", {
        "applications": page_obj, "page_obj": page_obj, "filter_form": form,
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


@require_http_methods(["GET", "POST"])
def application_create(request):
    form = ApplicationForm(request.POST or None)
    formset = ApplicationItemFormSet(request.POST or None)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        application = form.save()
        formset.instance = application
        formset.save()
        return redirect("applications:detail", application_id=application.pk)
    return render(request, "applications/application_form.html", {
        "form": form, "formset": formset, "is_create": True,
    })


@require_http_methods(["GET", "POST"])
def application_update(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    form = ApplicationForm(request.POST or None, instance=application)
    formset = ApplicationItemFormSet(request.POST or None, instance=application)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        return redirect("applications:detail", application_id=application.pk)
    return render(request, "applications/application_form.html", {
        "form": form, "formset": formset, "application": application,
    })
