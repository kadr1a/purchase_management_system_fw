"""Функции работы с коллекцией товаров."""

from models import Product


def add_product(
    products: list[Product],
    name: str,
    price: float,
    description: str = "",
) -> Product:
    """Создаёт товар, добавляет его в коллекцию и возвращает объект."""
    name = name.strip()
    if not name:
        raise ValueError("Название товара не может быть пустым.")
    if price <= 0:
        raise ValueError("Цена должна быть больше нуля.")
    product = Product(f"P{len(products) + 1:03d}", name, price, description)
    products.append(product)
    return product


def find_product(products: list[Product], product_id: str) -> Product | None:
    """Ищет товар по идентификатору."""
    return next((item for item in products if item.id == product_id), None)


def filter_products(
    products: list[Product], min_price: float = 0
) -> list[Product]:
    """Возвращает товары с ценой не ниже заданной."""
    return [item for item in products if item.price >= min_price]


def sort_products(
    products: list[Product], field: str = "name"
) -> list[Product]:
    """Сортирует товары по названию или цене."""
    if field not in {"name", "price"}:
        raise ValueError("Сортировка доступна по полям name и price.")
    return sorted(products, key=lambda item: getattr(item, field))


def show_products(products: list[Product]) -> None:
    """Выводит товары."""
    print("\n--- Товары ---")
    if not products:
        print("Список пуст.")
        return
    for product in products:
        print(product)
