"""Преобразование объектов предметной области в JSON и обратно."""

import json
from pathlib import Path
from typing import Any

from models import Application, Product, PurchaseOrder, Supplier

DATA_FILES = {
    "products": "products.json",
    "suppliers": "suppliers.json",
    "applications": "applications.json",
    "orders": "orders.json",
}


def _read_json(directory: Path, key: str) -> list[dict[str, Any]]:
    path = directory / DATA_FILES[key]
    if not path.exists():
        path.write_text("[]", encoding="utf-8")
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise ValueError(f"Не удалось прочитать {path}: {error}") from error
    if not isinstance(result, list):
        raise ValueError(f"Файл {path} должен содержать JSON-массив.")
    return result


def load_data(
    data_dir: str = "data",
) -> dict[str, list[Any]]:
    """Загружает JSON и восстанавливает объекты и связи между ними."""
    directory = Path(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    raw = {key: _read_json(directory, key) for key in DATA_FILES}

    products = [
        Product(item["id"], item["name"], item["price"],
                item.get("description", ""))
        for item in raw["products"]
    ]
    suppliers = [
        Supplier(item["id"], item["name"], item.get("contact", ""),
                 item["rating"])
        for item in raw["suppliers"]
    ]
    product_by_id = {item.id: item for item in products}
    supplier_by_id = {item.id: item for item in suppliers}

    applications: list[Application] = []
    for item in raw["applications"]:
        application = Application(item["id"], item["purpose"])
        for product_item in item.get("product_items", []):
            product = product_by_id.get(product_item["product_id"])
            if product is None:
                raise ValueError(
                    f"В заявке {application.id} указан неизвестный товар "
                    f"{product_item['product_id']}."
                )
            application.add_product(product, product_item["quantity"])
        application.status = item.get("status", "Черновик")
        applications.append(application)

    application_by_id = {item.id: item for item in applications}
    orders: list[PurchaseOrder] = []
    for item in raw["orders"]:
        application = application_by_id.get(item["application_id"])
        supplier = supplier_by_id.get(item["supplier_id"])
        if application is None or supplier is None:
            raise ValueError(
                f"Заказ {item['id']} ссылается на неизвестную заявку "
                "или поставщика."
            )
        orders.append(
            PurchaseOrder(
                item["id"], application, supplier,
                item.get("total"), item.get("status", "Оформлен")
            )
        )
    return {
        "products": products,
        "suppliers": suppliers,
        "applications": applications,
        "orders": orders,
    }


def save_data(data_dir: str, data: dict[str, list[Any]]) -> None:
    """Сохраняет объекты в JSON, используя ID для связей между сущностями."""
    directory = Path(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    serialized: dict[str, list[dict[str, Any]]] = {
        "products": [
            {"id": p.id, "name": p.name, "price": p.price,
             "description": p.description}
            for p in data["products"]
        ],
        "suppliers": [
            {"id": s.id, "name": s.name, "contact": s.contact,
             "rating": s.rating}
            for s in data["suppliers"]
        ],
        "applications": [
            {
                "id": a.id,
                "purpose": a.purpose,
                "product_items": [
                    {"product_id": p.id, "quantity": quantity}
                    for p, quantity in a.product_items
                ],
                "status": a.status,
            }
            for a in data["applications"]
        ],
        "orders": [
            {
                "id": o.id,
                "application_id": o.application.id,
                "supplier_id": o.supplier.id,
                "total": o.total,
                "status": o.status,
            }
            for o in data["orders"]
        ],
    }
    for key, filename in DATA_FILES.items():
        path = directory / filename
        path.write_text(
            json.dumps(serialized[key], ensure_ascii=False, indent=4),
            encoding="utf-8",
        )
