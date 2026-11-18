"""Представления заказов поставщикам, использующие SQLite."""

from django.shortcuts import render

from db.repository import ORDER_LIST_SQL, fetch_all, fetch_one


def orders(request):
    """Показывает заказы с данными связанных заявок и поставщиков."""
    items = fetch_all(ORDER_LIST_SQL)
    return render(request, "orders/order_list.html", {"orders": items})


def order_detail(request, order_id):
    """Передаёт заказ и сведения о заявке и поставщике в шаблон."""
    order = fetch_one(
        """
        SELECT po.id, po.total, po.status, a.id AS application_id,
               a.purpose, s.name AS supplier_name, s.contact
        FROM purchase_orders AS po
        JOIN applications AS a ON a.id = po.application_id
        JOIN suppliers AS s ON s.id = po.supplier_id
        WHERE po.id = ?
        """,
        (order_id,),
    )
    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
        status=404 if order is None else 200,
    )
