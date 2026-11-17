"""Функции оформления и отмены заказов."""

from uuid import uuid4

from applications import calculate_application_total


def create_order(
    orders: list[dict], application: dict, supplier: dict
) -> dict:
    """Создаёт заказ на основании согласованной заявки."""
    if application["status"] != "Согласована":
        raise ValueError("Заказ можно создать только по согласованной заявке.")
    order = {
        "id": f"O{uuid4().hex[:8].upper()}",
        "application_id": application["id"],
        "supplier_id": supplier["id"],
        "supplier_name": supplier["name"],
        "products": application["product_items"].copy(),
        "total": calculate_application_total(application),
        "status": "Оформлен",
    }
    orders.append(order)
    application["status"] = "Заказ оформлен"
    return order


def cancel_order(order: dict) -> None:
    """Отменяет заказ, если он ещё не отменён или завершён."""
    if order["status"] != "Оформлен":
        raise ValueError("Отменить можно только оформленный заказ.")
    order["status"] = "Отменён"
