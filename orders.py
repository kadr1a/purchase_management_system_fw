"""Функции работы с коллекцией заказов."""

from uuid import uuid4

from models import Application, PurchaseOrder, Supplier


def create_order(
    orders: list[PurchaseOrder],
    application: Application,
    supplier: Supplier,
) -> PurchaseOrder:
    """Создаёт заказ на основании согласованной заявки."""
    if application.status != "Согласована":
        raise ValueError("Заказ можно создать только по согласованной заявке.")
    order = PurchaseOrder(
        f"O{uuid4().hex[:8].upper()}", application, supplier
    )
    orders.append(order)
    application.status = "Заказ оформлен"
    return order


def cancel_order(order: PurchaseOrder) -> None:
    """Отменяет заказ методом объекта PurchaseOrder."""
    order.cancel()


def find_order(
    orders: list[PurchaseOrder], order_id: str
) -> PurchaseOrder | None:
    """Ищет заказ по идентификатору."""
    return next((item for item in orders if item.id == order_id), None)


def show_orders(orders: list[PurchaseOrder]) -> None:
    """Выводит заказы."""
    print("\n--- Заказы ---")
    if not orders:
        print("Список пуст.")
        return
    for order in orders:
        print(order)
