"""Вспомогательные функции для чтения JSON-данных в веб-представлениях."""
from pathlib import Path

from storage import load_data

BASE_DIR = Path(__file__).resolve().parent


def get_project_data():
    """Загружает сущности и связи из существующего JSON-хранилища ПР3."""
    return load_data(str(BASE_DIR / "data"))
