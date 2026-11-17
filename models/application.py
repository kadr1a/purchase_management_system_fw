"""Модель заявки на закупку."""

from .product import Product


class Application:
    """Заявка хранит назначение, товары с количеством и текущий статус."""

    def __init__(self, application_id: str, purpose: str) -> None:
        self.id = application_id
        self.purpose = purpose.strip()
        self.product_items: list[tuple[Product, int]] = []
        self.status = "Черновик"

    def add_product(self, product: Product, quantity: int) -> None:
        """Добавляет товар в черновик заявки."""
        if self.status != "Черновик":
            raise ValueError("Изменять можно только черновик заявки.")
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля.")
        self.product_items.append((product, quantity))

    def calculate_total(self) -> float:
        """Возвращает общую стоимость всех позиций заявки."""
        return round(
            sum(product.price * quantity
                for product, quantity in self.product_items),
            2,
        )

    def approve(self) -> None:
        """Согласовывает непустую заявку."""
        if self.status != "Черновик":
            raise ValueError("Согласовать можно только черновик заявки.")
        if not self.product_items:
            raise ValueError("Нельзя согласовать пустую заявку.")
        self.status = "Согласована"

    def __str__(self) -> str:
        return (
            f"{self.id}: {self.purpose} | позиций: "
            f"{len(self.product_items)} | {self.calculate_total():.2f} руб. "
            f"| статус: {self.status}"
        )
