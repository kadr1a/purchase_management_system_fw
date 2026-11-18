"""View-функции раздела заявок на закупку."""
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from web_utils import get_project_data


def applications(request):
    """Показывает заявки и их текущие статусы."""
    items = get_project_data()["applications"]
    rows = "".join(
        f'<tr><td>{escape(item.id)}</td><td>{escape(item.purpose)}</td>'
        f'<td>{len(item.product_items)}</td>'
        f'<td>{item.calculate_total():.2f} руб.</td>'
        f'<td><span class="badge text-bg-info">{escape(item.status)}</span></td>'
        f'<td><a href="/applications/{escape(item.id)}/">Подробнее</a></td></tr>'
        for item in items
    )
    if not rows:
        rows = '<tr><td colspan="6">Заявки пока не созданы.</td></tr>'
    content = f"""
    <h1>Заявки на закупку</h1>
    <p>Заявки содержат товары, количество и статус согласования.</p>
    <div class="table-responsive"><table class="table table-striped">
    <thead><tr><th>ID</th><th>Назначение</th><th>Позиций</th>
    <th>Сумма</th><th>Статус</th><th></th></tr></thead>
    <tbody>{rows}</tbody></table></div>
    """
    return HttpResponse(page("Заявки", content))


def application_detail(request, application_id):
    """Показывает состав и итоговую сумму заявки."""
    items = get_project_data()["applications"]
    application = next(
        (item for item in items if item.id == application_id), None
    )
    if application is None:
        content = '<h1>Заявка не найдена</h1><a href="/applications/">К списку</a>'
        return HttpResponse(page("Заявка не найдена", content), status=404)
    product_rows = "".join(
        f'<li class="list-group-item">{escape(product.name)} — '
        f'{quantity} шт. × {product.price:.2f} руб. = '
        f'{product.price * quantity:.2f} руб.</li>'
        for product, quantity in application.product_items
    )
    if not product_rows:
        product_rows = '<li class="list-group-item">В заявке нет товаров.</li>'
    content = f"""
    <h1>Заявка {escape(application.id)}</h1>
    <p><strong>Назначение:</strong> {escape(application.purpose)}</p>
    <p><strong>Статус:</strong> {escape(application.status)}</p>
    <h2 class="h4 mt-4">Состав заявки</h2>
    <ul class="list-group mb-3">{product_rows}</ul>
    <p class="fs-5"><strong>Итого: {application.calculate_total():.2f} руб.</strong></p>
    <a class="btn btn-outline-secondary" href="/applications/">К списку заявок</a>
    """
    return HttpResponse(page(f"Заявка {application.id}", content))
