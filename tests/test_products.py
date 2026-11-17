from models import Product
from products import add_product, filter_products, find_product, sort_products


def test_product_creation_and_string():
    product = Product("P001", "Монитор", 12000, "IPS")
    assert product.id == "P001"
    assert product.name == "Монитор"
    assert "12000.00" in str(product)


def test_add_product_returns_object():
    products = []
    product = add_product(products, "Монитор", 12000, "IPS")
    assert isinstance(product, Product)
    assert products[0] is product


def test_add_product_rejects_invalid_price():
    try:
        add_product([], "Монитор", 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка для нулевой цены")


def test_find_filter_and_sort_products():
    products = [Product("P1", "Мышь", 1000), Product("P2", "Монитор", 10000)]
    assert find_product(products, "P2").name == "Монитор"
    assert len(filter_products(products, 5000)) == 1
    assert sort_products(products, "price")[0].name == "Мышь"
