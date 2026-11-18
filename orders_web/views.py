"""View-функции раздела заказов поставщикам."""
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from web_utils import get_project_data


def orders(request):
    """Показывает оформленные и отменённые заказы."""
    items = get_project_data()["orders"]
    rows = "".join(
        f'<tr><td>{escape(item.id)}</td>'
        f'<td>{escape(item.application.id)}</td>'
        f'<td>{escape(item.supplier.name)}</td>'
        f'<td>{item.total:.2f} руб.</td>'
        f'<td>{escape(item.status)}</td>'
        f'<td><a href="/orders/{escape(item.id)}/">Подробнее</a></td></tr>'
        for item in items
    )
    if not rows:
        rows = '<tr><td colspan="6">Заказы пока не оформлены.</td></tr>'
    content = f"""
    <h1>Заказы поставщикам</h1>
    <p>Заказ связывает согласованную заявку с выбранным поставщиком.</p>
    <div class="table-responsive"><table class="table table-striped">
    <thead><tr><th>ID</th><th>Заявка</th><th>Поставщик</th>
    <th>Сумма</th><th>Статус</th><th></th></tr></thead>
    <tbody>{rows}</tbody></table></div>
    """
    return HttpResponse(page("Заказы", content))


def order_detail(request, order_id):
    """Показывает подробную информацию о заказе."""
    items = get_project_data()["orders"]
    order = next((item for item in items if item.id == order_id), None)
    if order is None:
        content = '<h1>Заказ не найден</h1><a href="/orders/">К списку</a>'
        return HttpResponse(page("Заказ не найден", content), status=404)
    content = f"""
    <h1>Заказ {escape(order.id)}</h1>
    <div class="card"><div class="card-body">
    <p><strong>Заявка:</strong> <a href="/applications/{escape(order.application.id)}/">
    {escape(order.application.id)} — {escape(order.application.purpose)}</a></p>
    <p><strong>Поставщик:</strong> <a href="/suppliers/{escape(order.supplier.id)}/">
    {escape(order.supplier.name)}</a></p>
    <p><strong>Сумма:</strong> {order.total:.2f} руб.</p>
    <p><strong>Статус:</strong> {escape(order.status)}</p>
    </div></div>
    <a class="btn btn-outline-secondary mt-3" href="/orders/">К списку заказов</a>
    """
    return HttpResponse(page(f"Заказ {order.id}", content))
