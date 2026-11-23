"""Главная страница и аналитика на Django ORM."""
from decimal import Decimal

from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render

from products_web.models import Product
from suppliers_web.models import Supplier
from applications_web.models import Application
from orders_web.models import PurchaseOrder


def index(request):
    stats = {
        "products_count": Product.objects.count(),
        "suppliers_count": Supplier.objects.count(),
        "applications_count": Application.objects.count(),
        "orders_count": PurchaseOrder.objects.count(),
        "active_order_total": (
            PurchaseOrder.objects.ordered()
            .aggregate(total=Coalesce(Sum("total"), Decimal("0.00")))["total"]
        ),
    }
    sections = [
        {"title": "Товары", "description": "Каталог и цены товаров",
         "count": stats["products_count"], "url_name": "products:list", "icon": "▦"},
        {"title": "Поставщики", "description": "Контакты и рейтинг поставщиков",
         "count": stats["suppliers_count"], "url_name": "suppliers:list", "icon": "◇"},
        {"title": "Заявки", "description": "Состав и статусы заявок",
         "count": stats["applications_count"], "url_name": "applications:list", "icon": "▤"},
        {"title": "Заказы", "description": "Заказы поставщикам",
         "count": stats["orders_count"], "url_name": "orders:list", "icon": "▣"},
    ]
    return render(request, "homepage/index.html", {"sections": sections, "stats": stats})


def statistics(request):
    stats = {
        "products_count": Product.objects.count(),
        "suppliers_count": Supplier.objects.count(),
        "applications_count": Application.objects.count(),
        "orders_count": PurchaseOrder.objects.count(),
        "active_order_total": (
            PurchaseOrder.objects.ordered()
            .aggregate(total=Coalesce(Sum("total"), Decimal("0.00")))["total"]
        ),
    }
    application_totals = (
        Application.objects.with_summary()
        .values("id", "purpose", "application_total")
        .order_by("-application_total", "id")
    )
    price_metrics = Product.objects.aggregate(
        average_price=Avg("price"),
        min_price=Min("price"),
        max_price=Max("price"),
    )
    return render(request, "homepage/statistics.html", {
        "stats": stats,
        "price_metrics": price_metrics,
        "application_totals": application_totals,
        "stat_items": [
            ("Товары", stats["products_count"]),
            ("Поставщики", stats["suppliers_count"]),
            ("Заявки", stats["applications_count"]),
            ("Заказы", stats["orders_count"]),
        ],
    })


def page_not_found(request, exception):
    """Отображает пользовательскую страницу 404."""
    return render(request, "404.html", status=404)
