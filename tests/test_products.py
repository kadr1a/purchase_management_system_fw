import pytest

from products import add_product, filter_products, find_product, sort_products


def test_add_product():
    products = []
    product = add_product(products, "Монитор", 12000, "IPS")
    assert product["id"] == "P001"
    assert products[0]["name"] == "Монитор"


def test_add_product_rejects_invalid_price():
    with pytest.raises(ValueError):
        add_product([], "Монитор", 0)


def test_find_filter_and_sort_products():
    products = [
        {"id": "P1", "name": "Мышь", "price": 1000},
        {"id": "P2", "name": "Монитор", "price": 10000},
    ]
    assert find_product(products, "P2")["name"] == "Монитор"
    assert len(filter_products(products, 5000)) == 1
    assert sort_products(products, "price")[0]["name"] == "Мышь"
