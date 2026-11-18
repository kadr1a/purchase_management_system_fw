"""Представления главной страницы веб-интерфейса."""
from django.shortcuts import render

from web_utils import get_project_data


def index(request):
    """Показывает главную страницу и краткую статистику разделов."""
    data = get_project_data()
    sections = [
        {"title": "Товары", "description": "Каталог и цены товаров", "count": len(data["products"]), "url_name": "products:list", "icon": "▦"},
        {"title": "Поставщики", "description": "Контакты и рейтинг поставщиков", "count": len(data["suppliers"]), "url_name": "suppliers:list", "icon": "◇"},
        {"title": "Заявки", "description": "Состав и статусы заявок", "count": len(data["applications"]), "url_name": "applications:list", "icon": "▤"},
        {"title": "Заказы", "description": "Заказы поставщикам", "count": len(data["orders"]), "url_name": "orders:list", "icon": "▣"},
    ]
    return render(request, "homepage/index.html", {"sections": sections})


def page_not_found(request, exception):
    """Отображает общую страницу 404 через систему шаблонов."""
    return render(request, "404.html", status=404)
