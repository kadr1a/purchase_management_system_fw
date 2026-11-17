"""Функции создания и обработки заявок на закупку."""

from uuid import uuid4


def create_application(applications: list[dict], purpose: str) -> dict:
    """Создаёт новую заявку со статусом «Черновик»."""
    purpose = purpose.strip()
    if not purpose:
        raise ValueError("Укажите назначение заявки.")
    application = {
        "id": f"A{uuid4().hex[:8].upper()}",
        "purpose": purpose,
        "product_items": [],
        "status": "Черновик",
    }
    applications.append(application)
    return application


def add_product_to_application(
    application: dict, product: dict, quantity: int
) -> None:
    """Добавляет товар и количество в заявку."""
    if application["status"] != "Черновик":
        raise ValueError("Изменять можно только черновик заявки.")
    if quantity <= 0:
        raise ValueError("Количество должно быть больше нуля.")
    application["product_items"].append(
        {
            "product_id": product["id"],
            "product_name": product["name"],
            "price": product["price"],
            "quantity": quantity,
        }
    )


def calculate_application_total(application: dict) -> float:
    """Рассчитывает общую сумму заявки."""
    return round(
        sum(
            item["price"] * item["quantity"]
            for item in application["product_items"]
        ),
        2,
    )


def approve_application(application: dict) -> None:
    """Согласовывает заявку, если в ней есть товары."""
    if application["status"] != "Черновик":
        raise ValueError("Согласовать можно только черновик заявки.")
    if not application["product_items"]:
        raise ValueError("Нельзя согласовать пустую заявку.")
    application["status"] = "Согласована"
