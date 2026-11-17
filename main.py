"""Начальный консольный сценарий системы управления закупками (ПР1)."""

from utils import calculate_total, check_budget, validate_purchase_data


def main() -> None:
    print("=== Система управления закупками ===")

    product_name = input("Введите название товара: ").strip()
    unit_price = float(input("Введите цену одной единицы товара (руб.): "))
    quantity = int(input("Введите необходимое количество: "))
    budget = float(input("Введите доступный бюджет (руб.): "))

    if not product_name:
        print("Ошибка: название товара не должно быть пустым.")
        return

    if not validate_purchase_data(unit_price, quantity, budget):
        print("Ошибка: цена и количество должны быть больше нуля, бюджет не может быть отрицательным.")
        return

    total = calculate_total(unit_price, quantity)

    print("\n--- Результат проверки заявки ---")
    print(f"Товар: {product_name}")
    print(f"Цена за единицу: {unit_price:.2f} руб.")
    print(f"Количество: {quantity}")
    print(f"Предварительная сумма заявки: {total:.2f} руб.")
    print(f"Доступный бюджет: {budget:.2f} руб.")
    print(f"Результат: {check_budget(total, budget)}")


if __name__ == "__main__":
    main()
