"""Консольное приложение «Система управления закупками» (ПР3)."""

from applications import (
    add_product_to_application,
    approve_application,
    create_application,
    find_application,
    show_applications,
)
from orders import cancel_order, create_order, find_order, show_orders
from products import (
    add_product,
    filter_products,
    find_product,
    show_products,
    sort_products,
)
from storage import load_data, save_data
from suppliers import (
    add_supplier,
    find_supplier,
    show_suppliers,
    sort_suppliers,
)
from utils import read_float, read_int

DATA_DIR = "data"


def run() -> None:
    """Загружает данные и запускает главное меню."""
    data = load_data(DATA_DIR)
    while True:
        print("\n=== Система управления закупками ===")
        print("1. Показать товары")
        print("2. Добавить товар")
        print("3. Найти товар по ID")
        print("4. Показать поставщиков")
        print("5. Добавить поставщика")
        print("6. Создать заявку")
        print("7. Добавить товар в заявку")
        print("8. Согласовать заявку")
        print("9. Создать заказ по заявке")
        print("10. Показать заявки и заказы")
        print("11. Отменить заказ")
        print("12. Фильтровать товары по минимальной цене")
        print("13. Сортировать товары")
        print("14. Сортировать поставщиков по рейтингу")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_products(data["products"])
            elif choice == "2":
                product = add_product(
                    data["products"], input("Название: "),
                    read_float("Цена: "), input("Описание: ")
                )
                save_data(DATA_DIR, data)
                print(f"Добавлен товар: {product}")
            elif choice == "3":
                product = find_product(data["products"], input("ID товара: "))
                print(product if product else "Товар не найден.")
            elif choice == "4":
                show_suppliers(data["suppliers"])
            elif choice == "5":
                supplier = add_supplier(
                    data["suppliers"], input("Название поставщика: "),
                    input("Контакт: "), read_int("Рейтинг (1–5): ")
                )
                save_data(DATA_DIR, data)
                print(f"Добавлен поставщик: {supplier}")
            elif choice == "6":
                application = create_application(
                    data["applications"], input("Название/цель заявки: ")
                )
                save_data(DATA_DIR, data)
                print(f"Создана заявка: {application.id}")
            elif choice == "7":
                application = find_application(
                    data["applications"], input("ID заявки: ")
                )
                product = find_product(
                    data["products"], input("ID товара: ")
                )
                if application is None or product is None:
                    print("Заявка или товар не найдены.")
                else:
                    add_product_to_application(
                        application, product, read_int("Количество: ")
                    )
                    save_data(DATA_DIR, data)
                    print("Товар добавлен в заявку.")
            elif choice == "8":
                application = find_application(
                    data["applications"], input("ID заявки: ")
                )
                if application is None:
                    print("Заявка не найдена.")
                else:
                    approve_application(application)
                    save_data(DATA_DIR, data)
                    print("Заявка согласована.")
            elif choice == "9":
                application = find_application(
                    data["applications"], input("ID заявки: ")
                )
                supplier = find_supplier(
                    data["suppliers"], input("ID поставщика: ")
                )
                if application is None or supplier is None:
                    print("Заявка или поставщик не найдены.")
                else:
                    order = create_order(data["orders"], application, supplier)
                    save_data(DATA_DIR, data)
                    print(f"Создан заказ: {order.id}")
            elif choice == "10":
                show_applications(data["applications"])
                show_orders(data["orders"])
            elif choice == "11":
                order = find_order(data["orders"], input("ID заказа: "))
                if order is None:
                    print("Заказ не найден.")
                else:
                    cancel_order(order)
                    save_data(DATA_DIR, data)
                    print("Заказ отменён.")
            elif choice == "12":
                min_price = read_float("Минимальная цена: ")
                show_products(filter_products(data["products"], min_price))
            elif choice == "13":
                field = input("Сортировать по name или price: ").strip()
                show_products(sort_products(data["products"], field))
            elif choice == "14":
                show_suppliers(sort_suppliers(data["suppliers"]))
            elif choice == "0":
                save_data(DATA_DIR, data)
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Нет такого пункта меню.")
        except (ValueError, KeyError) as error:
            print(f"Не удалось выполнить операцию: {error}")


if __name__ == "__main__":
    run()
