"""Интеграционные проверки моделей, связей и ORM-представлений."""
from decimal import Decimal

import pytest
from django.test import Client
from django.urls import reverse

from products_web.models import Product
from suppliers_web.models import Supplier
from applications_web.models import Application, ApplicationItem
from orders_web.models import PurchaseOrder

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_data():
    product = Product.objects.create(
        id="T001", name="Тестовый монитор", price=Decimal("1200.00"),
        description="Экран для офиса",
    )
    supplier = Supplier.objects.create(
        id="S900", name="Тестовый поставщик", contact="test@example.com",
        rating=5,
    )
    application = Application.objects.create(
        id="A900", purpose="Оборудование кабинета", status="Согласована",
    )
    ApplicationItem.objects.create(
        application=application, product=product, quantity=2,
    )
    order = PurchaseOrder.objects.create(
        id="O900", application=application, supplier=supplier,
        total=Decimal("2400.00"),
    )
    return product, supplier, application, order


def test_foreign_keys_and_reverse_relations(sample_data):
    product, supplier, application, order = sample_data
    assert order.application == application
    assert order.supplier == supplier
    assert application.items.get().product == product
    assert product.application_items.get().application == application
    assert supplier.purchase_orders.get() == order


def test_product_search_and_invalid_price():
    Product.objects.create(id="T002", name="Мышь", price=Decimal("50"))
    client = Client()
    response = client.get(reverse("products:list"), {"q": "мыш"})
    assert response.status_code == 200
    assert "Мышь" in response.content.decode()
    invalid = client.get(reverse("products:list"), {"min_price": "abc"})
    assert invalid.status_code == 200
    assert "корректную" in invalid.content.decode()


def test_application_aggregate_and_related_detail(sample_data):
    _, _, application, _ = sample_data
    response = Client().get(reverse("applications:list"))
    assert response.status_code == 200
    assert "2400,00" in response.content.decode()
    detail = Client().get(
        reverse("applications:detail", args=[application.pk]),
    )
    assert detail.status_code == 200
    assert "Тестовый монитор" in detail.content.decode()


def test_supplier_filter_and_order_search(sample_data):
    _, supplier, _, order = sample_data
    client = Client()
    response = client.get(reverse("suppliers:list"), {"min_rating": "5"})
    assert supplier.name in response.content.decode()
    orders = client.get(reverse("orders:list"), {"q": supplier.name})
    assert order.pk in orders.content.decode()


def test_order_cancel_method(sample_data):
    order = sample_data[3]
    order.cancel()
    order.refresh_from_db()
    assert order.status == "Отменён"
    with pytest.raises(ValueError):
        order.cancel()


def test_exclude_and_aggregate_queries(sample_data):
    Product.objects.create(id="T003", name="Дешёвый кабель",
                           price=Decimal("10.00"))
    assert Product.objects.exclude(price__lt=100).count() == 1
    assert Product.objects.filter(name__istartswith="Тест").get().pk == "T001"
    assert Product.objects.aggregate(total=__import__(
        "django.db.models", fromlist=["Sum"]
    ).Sum("price"))["total"] == Decimal("1210")


def test_supplier_exact_name_filter_and_invalid_rating(sample_data):
    supplier = sample_data[1]
    client = Client()
    exact = client.get(
        reverse("suppliers:list"), {"exact_name": supplier.name.lower()},
    )
    assert exact.status_code == 200
    assert supplier.name in exact.content.decode()
    invalid = client.get(reverse("suppliers:list"), {"min_rating": "9"})
    assert invalid.status_code == 200
    assert "от 1 до 5" in invalid.content.decode()


def test_product_pagination_and_safe_sorting():
    for index in range(8):
        Product.objects.create(
            id=f"PG{index}",
            name=f"Позиция {index}",
            price=Decimal("100.00") + index,
        )
    response = Client().get(
        reverse("products:list"), {"page": "2", "sort": "not-allowed"},
    )
    assert response.status_code == 200
    assert response.context["page_obj"].number == 2
    assert "Страница 2" in response.content.decode()


def test_application_exclude_status(sample_data):
    response = Client().get(
        reverse("applications:list"), {"exclude_status": "Согласована"},
    )
    assert response.status_code == 200
    assert "Оборудование кабинета" not in response.content.decode()


def test_statistics_use_orm_aggregates(sample_data):
    response = Client().get(reverse("homepage:statistics"))
    html = response.content.decode()
    assert response.status_code == 200
    assert "Цены каталога" in html
    assert "Минимальная цена" in html
    assert "Средняя цена" in html
    assert "Максимальная цена" in html
