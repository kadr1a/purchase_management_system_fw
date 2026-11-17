"""Модель заказа поставщику."""

from .application import Application
from .supplier import Supplier


class PurchaseOrder:
    """Заказ связывает согласованную заявку с выбранным поставщиком."""

    def __init__(
        self,
        order_id: str,
        application: Application,
        supplier: Supplier,
        total: float | None = None,
        status: str = "Оформлен",
    ) -> None:
        self.id = order_id
        self.application = application
        self.supplier = supplier
        self.total = (
            application.calculate_total() if total is None else round(total, 2)
        )
        self.status = status

    def cancel(self) -> None:
        """Отменяет оформленный заказ."""
        if self.status != "Оформлен":
            raise ValueError("Отменить можно только оформленный заказ.")
        self.status = "Отменён"

    def __str__(self) -> str:
        return (
            f"{self.id}: заявка {self.application.id} — "
            f"{self.supplier.name} | {self.total:.2f} руб. "
            f"| статус: {self.status}"
        )
