"""Подключение к SQLite для системы управления закупками."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "procurement.sqlite3"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection():
    """Открывает соединение и включает контроль внешних ключей."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Создаёт таблицы по SQL-схеме, если их ещё нет."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection = get_connection()
    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()
