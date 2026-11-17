"""Функции работы с поставщиками."""


def add_supplier(
    suppliers: list[dict],
    name: str,
    contact: str,
    rating: int,
) -> dict:
    """Добавляет поставщика."""
    name = name.strip()
    if not name:
        raise ValueError("Название поставщика не может быть пустым.")
    if not 1 <= rating <= 5:
        raise ValueError("Рейтинг должен быть от 1 до 5.")
    supplier = {
        "id": f"S{len(suppliers) + 1:03d}",
        "name": name,
        "contact": contact.strip(),
        "rating": rating,
    }
    suppliers.append(supplier)
    return supplier


def find_supplier(suppliers: list[dict], supplier_id: str) -> dict | None:
    """Ищет поставщика по ID."""
    return next(
        (supplier for supplier in suppliers if supplier["id"] == supplier_id),
        None,
    )


def sort_suppliers(suppliers: list[dict]) -> list[dict]:
    """Сортирует поставщиков по рейтингу от большего к меньшему."""
    return sorted(suppliers, key=lambda item: item["rating"], reverse=True)
