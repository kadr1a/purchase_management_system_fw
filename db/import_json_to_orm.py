"""Перенос исходных JSON-данных в таблицы Django ORM.

Запуск: python db/import_json_to_orm.py
Повторный запуск безопасен: записи обновляются по исходным ID.
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "procurement.settings")

import django  # noqa: E402

django.setup()

from django.db import transaction  # noqa: E402
from storage import load_data  # noqa: E402
from products_web.models import Product  # noqa: E402
from suppliers_web.models import Supplier  # noqa: E402
from applications_web.models import Application, ApplicationItem  # noqa: E402
from orders_web.models import PurchaseOrder  # noqa: E402


def import_json():
    data = load_data(str(PROJECT_ROOT / "data"))
    with transaction.atomic():
        for item in data["products"]:
            Product.objects.update_or_create(
                pk=item.id,
                defaults={
                    "name": item.name,
                    "price": item.price,
                    "description": item.description,
                },
            )
        for item in data["suppliers"]:
            Supplier.objects.update_or_create(
                pk=item.id,
                defaults={
                    "name": item.name,
                    "contact": item.contact,
                    "rating": item.rating,
                },
            )
        for item in data["applications"]:
            application, _ = Application.objects.update_or_create(
                pk=item.id,
                defaults={"purpose": item.purpose, "status": item.status},
            )
            ApplicationItem.objects.filter(application=application).delete()
            for product, quantity in item.product_items:
                ApplicationItem.objects.update_or_create(
                    application=application,
                    product_id=product.id,
                    defaults={"quantity": quantity},
                )
        for item in data["orders"]:
            PurchaseOrder.objects.update_or_create(
                pk=item.id,
                defaults={
                    "application_id": item.application.id,
                    "supplier_id": item.supplier.id,
                    "total": item.total,
                    "status": item.status,
                },
            )
    return {
        "products": Product.objects.count(),
        "suppliers": Supplier.objects.count(),
        "applications": Application.objects.count(),
        "orders": PurchaseOrder.objects.count(),
    }


if __name__ == "__main__":
    print("Импорт завершён:", import_json())
