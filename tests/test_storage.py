from applications import (
    add_product_to_application,
    approve_application,
    create_application,
)
from models import Product
from orders import create_order
from storage import load_data, save_data
from suppliers import add_supplier


def test_load_and_save_json_as_objects(tmp_path):
    data = load_data(str(tmp_path))
    product = Product("P001", "Товар", 100)
    supplier = add_supplier(data["suppliers"], "Поставщик", "mail", 5)
    data["products"].append(product)
    application = create_application(data["applications"], "Проверка")
    add_product_to_application(application, product, 2)
    approve_application(application)
    order = create_order(data["orders"], application, supplier)
    save_data(str(tmp_path), data)

    loaded = load_data(str(tmp_path))
    loaded_application = loaded["applications"][0]
    loaded_order = loaded["orders"][0]
    assert isinstance(loaded["products"][0], Product)
    assert loaded_application.product_items[0][0] is loaded["products"][0]
    assert loaded_order.application is loaded_application
    assert loaded_order.supplier is loaded["suppliers"][0]
    assert loaded_order.total == order.total
