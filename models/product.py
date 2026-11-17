"""Модель товара."""


class Product:
    """Товар, который может быть включён в заявку на закупку."""

    def __init__(
        self, product_id: str, name: str, price: float, description: str = ""
    ) -> None:
        self.id = product_id
        self.name = name.strip()
        self.price = round(float(price), 2)
        self.description = description.strip()

    def __str__(self) -> str:
        return f"{self.id}: {self.name} — {self.price:.2f} руб."
