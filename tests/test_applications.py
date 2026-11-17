import pytest

from applications import (
    add_product_to_application,
    approve_application,
    calculate_application_total,
    create_application,
)
from models import Application, Product


def test_application_total_and_approval():
    application = create_application([], "Оснащение рабочего места")
    product = Product("P1", "Монитор", 5000)
    add_product_to_application(application, product, 2)
    assert isinstance(application, Application)
    assert application.product_items[0][0] is product
    assert calculate_application_total(application) == 10000
    approve_application(application)
    assert application.status == "Согласована"


def test_empty_application_cannot_be_approved():
    application = create_application([], "Закупка")
    with pytest.raises(ValueError):
        approve_application(application)


def test_approved_application_cannot_be_changed():
    application = create_application([], "Закупка")
    product = Product("P1", "Мышь", 1000)
    add_product_to_application(application, product, 1)
    application.approve()
    with pytest.raises(ValueError):
        application.add_product(product, 1)
