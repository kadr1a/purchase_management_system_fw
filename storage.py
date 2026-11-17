"""Загрузка и сохранение данных в JSON.""" 

import json
from pathlib import Path
from typing import Any

DATA_FILES = {
    "products": "products.json",
    "suppliers": "suppliers.json",
    "applications": "applications.json",
    "orders": "orders.json",
}


def load_data(data_dir: str = "data") -> dict[str, list[dict[str, Any]]]:
    """Загружает все наборы данных; отсутствующие файлы создаются пустыми."""
    directory = Path(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    result = {}
    for key, filename in DATA_FILES.items():
        path = directory / filename
        if not path.exists():
            path.write_text("[]", encoding="utf-8")
        try:
            result[key] = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as error:
            raise ValueError(
                f"Не удалось прочитать {path}: {error}"
            ) from error
        if not isinstance(result[key], list):
            raise ValueError(f"Файл {path} должен содержать JSON-массив.")
    return result


def save_data(
    data_dir: str, data: dict[str, list[dict[str, Any]]]
) -> None:
    """Сохраняет все наборы данных в отдельные JSON-файлы."""
    directory = Path(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    for key, filename in DATA_FILES.items():
        path = directory / filename
        path.write_text(
            json.dumps(data[key], ensure_ascii=False, indent=4),
            encoding="utf-8",
        )
