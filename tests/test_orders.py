import pytest

from applications import (
    add_product_to_application,
    approve_application,
    create_application,
)
from models import Product, PurchaseOrder, Supplier
from orders import cancel_order, create_order


def test_create_and_cancel_order():
    application = create_application([], "Закупка оборудования")
    add_product_to_application(application, Product("P1", "Мышь", 1000), 3)
    approve_application(application)
    supplier = Supplier("S1", "Поставщик", "contact", 5)
    order = create_order([], application, supplier)
    assert isinstance(order, PurchaseOrder)
    assert order.total == 3000
    assert order.application is application
    assert order.supplier is supplier
    cancel_order(order)
    assert order.status == "Отменён"


def test_order_requires_approved_application():
    application = create_application([], "Закупка")
    supplier = Supplier("S1", "Поставщик", "contact", 5)
    with pytest.raises(ValueError):
        create_order([], application, supplier)
