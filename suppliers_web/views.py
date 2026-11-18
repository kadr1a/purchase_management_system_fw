"""View-функции раздела поставщиков."""
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from web_utils import get_project_data


def suppliers(request):
    """Показывает список поставщиков."""
    items = get_project_data()["suppliers"]
    rows = "".join(
        f'<tr><td>{escape(item.id)}</td><td>{escape(item.name)}</td>'
        f'<td>{escape(item.contact)}</td><td>{item.rating}/5</td>'
        f'<td><a href="/suppliers/{escape(item.id)}/">Подробнее</a></td></tr>'
        for item in items
    )
    if not rows:
        rows = '<tr><td colspan="5">Поставщики пока не добавлены.</td></tr>'
    content = f"""
    <h1>Поставщики</h1>
    <p>Организации, у которых система позволяет оформлять закупки.</p>
    <div class="table-responsive"><table class="table table-striped">
    <thead><tr><th>ID</th><th>Название</th><th>Контакт</th>
    <th>Рейтинг</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
    """
    return HttpResponse(page("Поставщики", content))


def supplier_detail(request, supplier_id):
    """Показывает информацию о выбранном поставщике."""
    items = get_project_data()["suppliers"]
    supplier = next((item for item in items if item.id == supplier_id), None)
    if supplier is None:
        content = '<h1>Поставщик не найден</h1><a href="/suppliers/">К списку</a>'
        return HttpResponse(page("Поставщик не найден", content), status=404)
    content = f"""
    <h1>{escape(supplier.name)}</h1>
    <div class="card"><div class="card-body">
    <p><strong>ID:</strong> {escape(supplier.id)}</p>
    <p><strong>Контакт:</strong> {escape(supplier.contact)}</p>
    <p><strong>Рейтинг:</strong> {supplier.rating}/5</p>
    </div></div>
    <a class="btn btn-outline-secondary mt-3" href="/suppliers/">К поставщикам</a>
    """
    return HttpResponse(page(supplier.name, content))
