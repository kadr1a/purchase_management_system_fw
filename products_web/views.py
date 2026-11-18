"""View-функции каталога товаров."""
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from web_utils import get_project_data


def products(request):
    """Показывает список товаров из JSON."""
    items = get_project_data()["products"]
    rows = "".join(
        f'<tr><td>{escape(item.id)}</td><td>{escape(item.name)}</td>'
        f'<td>{item.price:.2f} руб.</td>'
        f'<td><a href="/products/{escape(item.id)}/">Подробнее</a></td></tr>'
        for item in items
    )
    if not rows:
        rows = '<tr><td colspan="4">Товары пока не добавлены.</td></tr>'
    content = f"""
    <h1>Товары</h1>
    <p>Каталог товаров, доступных для включения в заявки на закупку.</p>
    <div class="table-responsive"><table class="table table-striped">
    <thead><tr><th>ID</th><th>Название</th><th>Цена</th><th></th></tr></thead>
    <tbody>{rows}</tbody></table></div>
    """
    return HttpResponse(page("Товары", content))


def product_detail(request, product_id):
    """Показывает карточку выбранного товара."""
    items = get_project_data()["products"]
    product = next((item for item in items if item.id == product_id), None)
    if product is None:
        content = '<h1>Товар не найден</h1><a href="/products/">К каталогу</a>'
        return HttpResponse(page("Товар не найден", content), status=404)
    content = f"""
    <h1>{escape(product.name)}</h1>
    <div class="card"><div class="card-body">
    <p><strong>Идентификатор:</strong> {escape(product.id)}</p>
    <p><strong>Цена:</strong> {product.price:.2f} руб.</p>
    <p><strong>Описание:</strong> {escape(product.description or "Не указано")}</p>
    </div></div>
    <a class="btn btn-outline-secondary mt-3" href="/products/">К списку товаров</a>
    """
    return HttpResponse(page(product.name, content))
