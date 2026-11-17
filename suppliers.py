"""Функции работы с коллекцией поставщиков."""

from models import Supplier


def add_supplier(
    suppliers: list[Supplier], name: str, contact: str, rating: int
) -> Supplier:
    """Создаёт поставщика и добавляет его в коллекцию."""
    name = name.strip()
    if not name:
        raise ValueError("Название поставщика не может быть пустым.")
    if not 1 <= rating <= 5:
        raise ValueError("Рейтинг должен быть от 1 до 5.")
    supplier = Supplier(
        f"S{len(suppliers) + 1:03d}", name, contact, rating
    )
    suppliers.append(supplier)
    return supplier


def find_supplier(
    suppliers: list[Supplier], supplier_id: str
) -> Supplier | None:
    """Ищет поставщика по идентификатору."""
    return next(
        (supplier for supplier in suppliers if supplier.id == supplier_id),
        None,
    )


def sort_suppliers(suppliers: list[Supplier]) -> list[Supplier]:
    """Сортирует поставщиков по рейтингу по убыванию."""
    return sorted(suppliers, key=lambda item: item.rating, reverse=True)


def show_suppliers(suppliers: list[Supplier]) -> None:
    """Выводит поставщиков."""
    print("\n--- Поставщики ---")
    if not suppliers:
        print("Список пуст.")
        return
    for supplier in suppliers:
        print(supplier)
