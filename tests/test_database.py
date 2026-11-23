"""Проверки слоя SQLite и импорта данных в изолированной тестовой БД."""

import sqlite3

import pytest

from db import database
from db.import_json import import_json


@pytest.fixture
def isolated_sqlite_database(monkeypatch, tmp_path):
    test_database = tmp_path / "procurement-test.sqlite3"
    monkeypatch.setattr(database, "DB_PATH", test_database)
    return test_database


def test_json_data_imports_to_sqlite(isolated_sqlite_database):
    """Импорт создаёт таблицы и переносит записи JSON в отдельную БД."""
    import_json()
    connection = sqlite3.connect(isolated_sqlite_database)
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


def test_schema_initialization_is_repeatable(isolated_sqlite_database):
    """Схему можно применить повторно без удаления существующих таблиц."""
    database.initialize_database()
    database.initialize_database()
    connection = sqlite3.connect(isolated_sqlite_database)
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
