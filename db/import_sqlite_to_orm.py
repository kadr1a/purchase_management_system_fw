"""Перенос записей из SQLite ПР7 в таблицы Django ORM.

Сначала выполните: python manage.py migrate
Затем: python db/import_sqlite_to_orm.py

Исходная БД не изменяется. Повторный запуск обновляет объекты по PK.
"""
import os
import sqlite3
import sys
from decimal import Decimal
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DB = PROJECT_ROOT / "data" / "procurement.sqlite3"
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "procurement.settings")

import django  # noqa: E402

django.setup()

from django.db import transaction  # noqa: E402
from products_web.models import Product  # noqa: E402
from suppliers_web.models import Supplier  # noqa: E402
from applications_web.models import Application, ApplicationItem  # noqa: E402
from orders_web.models import PurchaseOrder  # noqa: E402


def import_sqlite():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    source = sqlite3.connect(SOURCE_DB)
    source.row_factory = sqlite3.Row
    try:
        with transaction.atomic():
            for row in source.execute(
                "SELECT id, name, price, description FROM products"
            ):
                Product.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "price": Decimal(str(row["price"])),
                        "description": row["description"],
                    },
                )

            for row in source.execute(
                "SELECT id, name, contact, rating FROM suppliers"
            ):
                Supplier.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "contact": row["contact"],
                        "rating": row["rating"],
                    },
                )

            for row in source.execute(
                "SELECT id, purpose, status FROM applications"
            ):
                Application.objects.update_or_create(
                    pk=row["id"],
                    defaults={"purpose": row["purpose"], "status": row["status"]},
                )

            for row in source.execute(
                "SELECT id, application_id, product_id, quantity "
                "FROM application_items"
            ):
                ApplicationItem.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "application_id": row["application_id"],
                        "product_id": row["product_id"],
                        "quantity": row["quantity"],
                    },
                )

            for row in source.execute(
                "SELECT id, application_id, supplier_id, total, status "
                "FROM purchase_orders"
            ):
                PurchaseOrder.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "application_id": row["application_id"],
                        "supplier_id": row["supplier_id"],
                        "total": Decimal(str(row["total"])),
                        "status": row["status"],
                    },
                )
    finally:
        source.close()

    return {
        "products": Product.objects.count(),
        "suppliers": Supplier.objects.count(),
        "applications": Application.objects.count(),
        "application_items": ApplicationItem.objects.count(),
        "orders": PurchaseOrder.objects.count(),
    }


if __name__ == "__main__":
    print("Перенос завершён:", import_sqlite())
