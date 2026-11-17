"""Вспомогательные функции для начального сценария ПР1."""


def calculate_total(unit_price: float, quantity: int) -> float:
    """Возвращает предварительную стоимость заявки."""
    return unit_price * quantity


def validate_purchase_data(unit_price: float, quantity: int, budget: float) -> bool:
    """Проверяет базовую корректность введённых данных."""
    return unit_price > 0 and quantity > 0 and budget >= 0


def check_budget(total: float, budget: float) -> str:
    """Определяет, укладывается ли заявка в доступный бюджет."""
    if total <= budget:
        return "Заявка укладывается в бюджет. Можно передать её на согласование."
    return "Сумма заявки превышает бюджет. Требуется корректировка."
