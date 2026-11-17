"""Функции работы с коллекцией заявок."""

from uuid import uuid4

from models import Application, Product


def create_application(
    applications: list[Application], purpose: str
) -> Application:
    """Создаёт заявку и добавляет её в коллекцию."""
    purpose = purpose.strip()
    if not purpose:
        raise ValueError("Укажите назначение заявки.")
    application = Application(
        f"A{uuid4().hex[:8].upper()}", purpose
    )
    applications.append(application)
    return application


def add_product_to_application(
    application: Application, product: Product, quantity: int
) -> None:
    """Добавляет товар в заявку через метод объекта Application."""
    application.add_product(product, quantity)


def calculate_application_total(application: Application) -> float:
    """Возвращает стоимость заявки."""
    return application.calculate_total()


def approve_application(application: Application) -> None:
    """Согласовывает заявку через метод объекта Application."""
    application.approve()


def find_application(
    applications: list[Application], application_id: str
) -> Application | None:
    """Ищет заявку по идентификатору."""
    return next(
        (item for item in applications if item.id == application_id), None
    )


def show_applications(applications: list[Application]) -> None:
    """Выводит заявки."""
    print("\n--- Заявки ---")
    if not applications:
        print("Список пуст.")
        return
    for application in applications:
        print(application)
