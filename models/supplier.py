"""Модель поставщика."""


class Supplier:
    """Поставщик товаров с контактами и рейтингом."""

    def __init__(
        self, supplier_id: str, name: str, contact: str, rating: int
    ) -> None:
        self.id = supplier_id
        self.name = name.strip()
        self.contact = contact.strip()
        self.rating = int(rating)

    def __str__(self) -> str:
        return (
            f"{self.id}: {self.name} | {self.contact} | "
            f"рейтинг: {self.rating}/5"
        )
