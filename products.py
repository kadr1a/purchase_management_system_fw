"""Функции работы с товарами."""

from typing import Any


def add_product(
    products: list[dict],
    name: str,
    price: float,
    description: str = "",
) -> dict:
    """Добавляет товар в список и возвращает его запись."""
    name = name.strip()
    if not name:
        raise ValueError("Название товара не может быть пустым.")
    if price <= 0:
        raise ValueError("Цена должна быть больше нуля.")
    product = {
        "id": f"P{len(products) + 1:03d}",
        "name": name,
        "price": round(price, 2),
        "description": description.strip(),
    }
    products.append(product)
    return product


def find_product(products: list[dict], product_id: str) -> dict | None:
    """Ищет товар по ID."""
    return next((item for item in products if item["id"] == product_id), None)


def filter_products(
    products: list[dict], min_price: float = 0
) -> list[dict]:
    """Возвращает товары с ценой не ниже заданной."""
    return [item for item in products if item["price"] >= min_price]


def sort_products(
    products: list[dict], field: str = "name"
) -> list[dict]:
    """Сортирует товары по названию или цене."""
    if field not in {"name", "price"}:
        raise ValueError("Сортировка доступна по полям name и price.")
    return sorted(products, key=lambda item: item[field])


def product_summary(product: dict[str, Any]) -> str:
    """Формирует краткое текстовое описание товара."""
    return f"{product['name']} — {product['price']:.2f} руб."
