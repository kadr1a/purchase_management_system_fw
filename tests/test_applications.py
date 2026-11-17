import pytest

from applications import (
    add_product_to_application,
    approve_application,
    calculate_application_total,
    create_application,
)


def test_application_total_and_approval():
    applications = []
    application = create_application(applications, "Оснащение рабочего места")
    product = {"id": "P1", "name": "Монитор", "price": 5000}
    add_product_to_application(application, product, 2)
    assert calculate_application_total(application) == 10000
    approve_application(application)
    assert application["status"] == "Согласована"


def test_empty_application_cannot_be_approved():
    application = create_application([], "Закупка")
    with pytest.raises(ValueError):
        approve_application(application)
