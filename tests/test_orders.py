import pytest

from applications import (
    add_product_to_application,
    approve_application,
    create_application,
)
from orders import cancel_order, create_order


def test_create_and_cancel_order():
    application = create_application([], "Закупка оборудования")
    product = {"id": "P1", "name": "Мышь", "price": 1000}
    add_product_to_application(application, product, 3)
    approve_application(application)
    supplier = {"id": "S1", "name": "Поставщик"}
    order = create_order([], application, supplier)
    assert order["total"] == 3000
    cancel_order(order)
    assert order["status"] == "Отменён"


def test_order_requires_approved_application():
    application = create_application([], "Закупка")
    with pytest.raises(ValueError):
        create_order([], application, {"id": "S1", "name": "Поставщик"})
