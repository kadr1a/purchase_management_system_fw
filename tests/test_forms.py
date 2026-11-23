"""Интеграционные тесты форм Django и пользовательских сценариев ПР11."""
from decimal import Decimal

import pytest
from django.test import Client
from django.urls import reverse

from products_web.models import Product
from suppliers_web.models import Supplier
from applications_web.models import Application, ApplicationItem
from orders_web.models import PurchaseOrder


pytestmark = pytest.mark.django_db


def test_product_model_form_create_and_validation():
    client = Client()
    url = reverse("products:create")
    bad = client.post(url, {"name": "A", "price": "0", "description": ""})
    assert bad.status_code == 200
    assert "Цена товара должна быть больше нуля" in bad.content.decode()
    response = client.post(url, {
        "name": "Новый принтер", "price": "15000.00",
        "description": "Лазерный принтер",
    })
    product = Product.objects.get(name="Новый принтер")
    assert response.status_code == 302
    assert product.id.startswith("PRD-")
    assert product.slug == "novyy-printer"


def test_product_update_uses_instance_without_duplicate():
    product = Product.objects.create(id="UPD1", name="Старый товар", price=Decimal("100"))
    response = Client().post(reverse("products:update", args=[product.pk]), {
        "name": "Обновлённый товар", "price": "125.00", "description": "Изменено",
    })
    product.refresh_from_db()
    assert response.status_code == 302
    assert Product.objects.count() == 1
    assert product.name == "Обновлённый товар"
    assert product.price == Decimal("125.00")


def test_supplier_form_create_and_rating_validation():
    client = Client()
    url = reverse("suppliers:create")
    invalid = client.post(url, {"name": "Поставщик", "contact": "", "rating": "8"})
    assert invalid.status_code == 200
    assert "Рейтинг должен быть от 1 до 5" in invalid.content.decode()
    response = client.post(url, {
        "name": "Новый поставщик", "contact": "mail@example.com", "rating": "4",
    })
    assert response.status_code == 302
    assert Supplier.objects.get(name="Новый поставщик").rating == 4


def test_application_form_creates_application_and_items():
    product = Product.objects.create(id="FORM-P", name="Кабель", price=Decimal("50.00"))
    response = Client().post(reverse("applications:create"), {
        "purpose": "Комплектующие для офиса",
        "status": Application.Status.DRAFT,
        "items-TOTAL_FORMS": "1",
        "items-INITIAL_FORMS": "0",
        "items-MIN_NUM_FORMS": "0",
        "items-MAX_NUM_FORMS": "1000",
        "items-0-product": str(product.pk),
        "items-0-quantity": "3",
    })
    assert response.status_code == 302
    application = Application.objects.get(purpose="Комплектующие для офиса")
    item = ApplicationItem.objects.get(application=application)
    assert item.quantity == 3
    assert item.unit_price == Decimal("50.00")
    assert item.line_total == Decimal("150.00")


def test_order_form_computes_total_and_cancel_is_post_only():
    product = Product.objects.create(id="ORD-P", name="Монитор", price=Decimal("900"))
    supplier = Supplier.objects.create(id="ORD-S", name="Поставщик", rating=5)
    application = Application.objects.create(id="ORD-A", purpose="Мониторы для отдела")
    ApplicationItem.objects.create(application=application, product=product, quantity=2)
    client = Client()
    response = client.post(reverse("orders:create"), {
        "application": application.pk, "supplier": supplier.pk,
    })
    order = PurchaseOrder.objects.get(application=application)
    assert response.status_code == 302
    assert order.total == Decimal("1800.00")
    assert client.get(reverse("orders:cancel", args=[order.pk])).status_code == 405
    assert client.post(reverse("orders:cancel", args=[order.pk])).status_code == 302
    order.refresh_from_db()
    assert order.status == PurchaseOrder.Status.CANCELLED


def test_product_image_upload_and_public_display(tmp_path, settings):
    from io import BytesIO
    from PIL import Image
    from django.core.files.uploadedfile import SimpleUploadedFile

    settings.MEDIA_ROOT = tmp_path
    image_buffer = BytesIO()
    Image.new("RGB", (4, 4), color="white").save(image_buffer, format="PNG")
    upload = SimpleUploadedFile("product.png", image_buffer.getvalue(), content_type="image/png")
    response = Client().post(reverse("products:create"), {
        "name": "Товар с изображением", "price": "99.00", "description": "",
        "image": upload,
    })
    product = Product.objects.get(name="Товар с изображением")
    assert response.status_code == 302
    assert product.image.name.startswith("products/")
    detail = Client().get(product.get_absolute_url())
    assert product.image.url in detail.content.decode()


def test_application_update_keeps_same_record_and_edits_purpose():
    application = Application.objects.create(
        id="APP-EDIT", purpose="Старая цель заявки",
    )
    response = Client().post(
        reverse("applications:update", args=[application.pk]),
        {
            "purpose": "Новая цель закупки",
            "status": Application.Status.DRAFT,
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
            "items-0-product": "",
            "items-0-quantity": "",
        },
    )
    application.refresh_from_db()
    assert response.status_code == 302
    assert Application.objects.count() == 1
    assert application.purpose == "Новая цель закупки"
