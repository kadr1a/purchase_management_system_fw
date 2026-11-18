"""Представления главной страницы веб-интерфейса."""

from django.shortcuts import render

from db.repository import STATISTICS_SQL, fetch_all, fetch_one


def index(request):
    """Показывает разделы и статистику, полученную непосредственно из SQLite."""
    stats = fetch_one(STATISTICS_SQL)
    sections = [
        {
            "title": "Товары",
            "description": "Каталог и цены товаров",
            "count": stats["products_count"],
            "url_name": "products:list",
            "icon": "▦",
        },
        {
            "title": "Поставщики",
            "description": "Контакты и рейтинг поставщиков",
            "count": stats["suppliers_count"],
            "url_name": "suppliers:list",
            "icon": "◇",
        },
        {
            "title": "Заявки",
            "description": "Состав и статусы заявок",
            "count": stats["applications_count"],
            "url_name": "applications:list",
            "icon": "▤",
        },
        {
            "title": "Заказы",
            "description": "Заказы поставщикам",
            "count": stats["orders_count"],
            "url_name": "orders:list",
            "icon": "▣",
        },
    ]
    return render(
        request,
        "homepage/index.html",
        {"sections": sections, "stats": stats},
    )


def statistics(request):
    """Отображает агрегированные показатели системы закупок."""
    stats = fetch_one(STATISTICS_SQL)
    application_totals = fetch_all_application_totals()
    return render(
        request,
        "homepage/statistics.html",
        {
            "stats": stats,
            "application_totals": application_totals,
            "stat_items": [
                ("Товары", stats["products_count"]),
                ("Поставщики", stats["suppliers_count"]),
                ("Заявки", stats["applications_count"]),
                ("Заказы", stats["orders_count"]),
            ],
        },
    )


def fetch_all_application_totals():
    """Получает сумму товарных позиций по каждой заявке."""
    query = """
    SELECT a.id, a.purpose,
           COALESCE(SUM(p.price * ai.quantity), 0) AS application_total
    FROM applications AS a
    LEFT JOIN application_items AS ai ON ai.application_id = a.id
    LEFT JOIN products AS p ON p.id = ai.product_id
    GROUP BY a.id, a.purpose
    ORDER BY application_total DESC
    """
    return fetch_all(query)


def page_not_found(request, exception):
    """Отображает общую страницу 404 через систему шаблонов."""
    return render(request, "404.html", status=404)
