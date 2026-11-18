"""Показывает структуру и количество записей в базе данных ПР7."""
import sqlite3
from pathlib import Path

SOURCE_DB = Path(__file__).resolve().parents[1] / "data" / "procurement.sqlite3"


def inspect():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")
    connection = sqlite3.connect(SOURCE_DB)
    try:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        for (table_name,) in tables:
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]
            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()
            print(f"{table_name}: {count} записей")
            print("  Поля:", ", ".join(column[1] for column in columns))
    finally:
        connection.close()


if __name__ == "__main__":
    inspect()
