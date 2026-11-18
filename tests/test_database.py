"""Проверки слоя SQLite и импорта данных."""

import sqlite3

from db.database import DB_PATH, initialize_database
from db.import_json import import_json


def test_json_data_imports_to_sqlite():
    """Импорт создаёт таблицы и переносит записи исходных JSON-файлов."""
    import_json()
    connection = sqlite3.connect(DB_PATH)
    try:
        products_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
        suppliers_count = connection.execute(
            "SELECT COUNT(*) FROM suppliers"
        ).fetchone()[0]
        assert products_count == 3
        assert suppliers_count == 2
        assert connection.execute(
            "PRAGMA foreign_key_list(application_items)"
        ).fetchall()
    finally:
        connection.close()


def test_schema_initialization_is_repeatable():
    """Схему можно применить повторно без удаления существующих таблиц."""
    initialize_database()
    initialize_database()
    connection = sqlite3.connect(DB_PATH)
    try:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert {
            "products",
            "suppliers",
            "applications",
            "application_items",
            "purchase_orders",
        }.issubset(tables)
    finally:
        connection.close()
