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
        id="A900", purpose="Оборудование кабинета", status=Application.Status.APPROVED,
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
    assert order.status == PurchaseOrder.Status.CANCELLED
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


def test_generated_application_item_total_uses_price_snapshot(sample_data):
    product, _, application, _ = sample_data
    item = application.items.get()

    assert item.unit_price == Decimal("1200.00")
    assert item.line_total == Decimal("2400.00")

    product.price = Decimal("1500.00")
    product.save(update_fields=["price"])
    item.refresh_from_db()

    assert item.unit_price == Decimal("1200.00")
    assert item.line_total == Decimal("2400.00")


def test_product_slug_and_absolute_url(sample_data):
    product = sample_data[0]

    assert product.slug == "testovyy-monitor"
    assert product.get_absolute_url() == f"/products/slug/{product.slug}/"
    response = Client().get(product.get_absolute_url())

    assert response.status_code == 200
    assert product.name in response.content.decode()


def test_duplicate_product_names_get_unique_slugs():
    first = Product.objects.create(
        id="SLUG1", name="Одинаковый товар", price=Decimal("10.00"),
    )
    second = Product.objects.create(
        id="SLUG2", name="Одинаковый товар", price=Decimal("12.00"),
    )

    assert first.slug == "odinakovyy-tovar"
    assert second.slug == "odinakovyy-tovar-2"


def test_global_context_processor_exposes_entity_counts(sample_data):
    response = Client().get(reverse("homepage:index"))

    assert response.status_code == 200
    assert response.context["procurement_counts"] == {
        "products": 1,
        "suppliers": 1,
        "applications": 1,
        "orders": 1,
    }


def test_admin_registers_all_procurement_models():
    from django.contrib import admin

    from applications_web.models import Application, ApplicationItem
    from orders_web.models import PurchaseOrder
    from suppliers_web.models import Supplier

    assert Product in admin.site._registry
    assert Supplier in admin.site._registry
    assert Application in admin.site._registry
    assert ApplicationItem in admin.site._registry
    assert PurchaseOrder in admin.site._registry


def test_admin_configuration_includes_search_filters_and_inlines():
    from django.contrib import admin

    from applications_web.models import Application
    from orders_web.models import PurchaseOrder
    from suppliers_web.models import Supplier

    assert admin.site._registry[Product].search_fields
    assert admin.site._registry[Supplier].list_filter == ("rating",)
    assert admin.site._registry[Application].inlines
    assert admin.site._registry[PurchaseOrder].list_select_related == (
        "application", "supplier",
    )


def test_admin_pages_open_for_superuser(sample_data):
    from django.contrib.auth import get_user_model

    user = get_user_model().objects.create_superuser(
        username="pr10-admin", email="admin@example.com", password="safe-test-password",
    )
    client = Client()
    client.force_login(user)

    admin_urls = [
        "/admin/",
        "/admin/products_web/product/",
        "/admin/suppliers_web/supplier/",
        "/admin/applications_web/application/",
        "/admin/applications_web/applicationitem/",
        "/admin/orders_web/purchaseorder/",
    ]
    for url in admin_urls:
        response = client.get(url)
        assert response.status_code == 200, url

    application = sample_data[2]
    inline_response = client.get(f"/admin/applications_web/application/{application.pk}/change/")
    assert inline_response.status_code == 200


def test_application_queryset_manager_summary(sample_data):
    application = sample_data[2]
    summarized = Application.objects.with_summary().get(pk=application.pk)

    assert summarized.item_count == 1
    assert summarized.application_total == Decimal("2400.00")


def test_application_queryset_summary_keeps_applications_without_items():
    application = Application.objects.create(
        id="A-EMPTY", purpose="Пустая заявка", status=Application.Status.DRAFT,
    )
    summarized = Application.objects.with_summary().get(pk=application.pk)

    assert summarized.item_count == 0
    assert summarized.application_total == Decimal("0.00")


def test_purchase_order_queryset_manager_filters_statuses(sample_data):
    order = sample_data[3]

    assert PurchaseOrder.objects.ordered().get() == order
    assert PurchaseOrder.objects.cancelled().count() == 0
    order.cancel()
    assert PurchaseOrder.objects.ordered().count() == 0
    assert PurchaseOrder.objects.cancelled().get() == order
