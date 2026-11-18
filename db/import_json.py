"""Однократный/повторяемый перенос данных из JSON в SQLite."""

from pathlib import Path

from storage import load_data

from db.database import get_connection, initialize_database


def import_json():
    """Переносит все JSON-сущности в SQLite в одной транзакции."""
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data = load_data(str(data_dir))
    initialize_database()
    connection = get_connection()
    try:
        connection.execute("DELETE FROM purchase_orders")
        connection.execute("DELETE FROM application_items")
        connection.execute("DELETE FROM applications")
        connection.execute("DELETE FROM suppliers")
        connection.execute("DELETE FROM products")

        connection.executemany(
            "INSERT INTO products (id, name, price, description) "
            "VALUES (?, ?, ?, ?)",
            [(p.id, p.name, p.price, p.description) for p in data["products"]],
        )
        connection.executemany(
            "INSERT INTO suppliers (id, name, contact, rating) VALUES (?, ?, ?, ?)",
            [(s.id, s.name, s.contact, s.rating) for s in data["suppliers"]],
        )
        connection.executemany(
            "INSERT INTO applications (id, purpose, status) VALUES (?, ?, ?)",
            [(a.id, a.purpose, a.status) for a in data["applications"]],
        )
        connection.executemany(
            "INSERT INTO application_items (application_id, product_id, quantity) "
            "VALUES (?, ?, ?)",
            [
                (a.id, product.id, quantity)
                for a in data["applications"]
                for product, quantity in a.product_items
            ],
        )
        connection.executemany(
            "INSERT INTO purchase_orders "
            "(id, application_id, supplier_id, total, status) "
            "VALUES (?, ?, ?, ?, ?)",
            [
                (o.id, o.application.id, o.supplier.id, o.total, o.status)
                for o in data["orders"]
            ],
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    import_json()
    print("Импорт JSON в SQLite завершён.")
