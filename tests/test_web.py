"""Проверки веб-интерфейса Django."""
import pytest
from django.test import Client, override_settings

pytestmark = pytest.mark.django_db


def test_main_page_returns_html():
    response = Client().get("/")
    assert response.status_code == 200
    assert "Система управления закупками" in response.content.decode()


@pytest.mark.parametrize(
    "url, heading",
    [
        ("/products/", "Товары"),
        ("/suppliers/", "Поставщики"),
        ("/applications/", "Заявки на закупку"),
        ("/orders/", "Заказы поставщикам"),
    ],
)
def test_section_pages(url, heading):
    response = Client().get(url)
    assert response.status_code == 200
    assert heading in response.content.decode()


def test_unknown_product_returns_404():
    response = Client().get("/products/UNKNOWN/")
    assert response.status_code == 404


@override_settings(DEBUG=False)
def test_custom_404_page():
    response = Client().get("/this-page-does-not-exist/")
    assert response.status_code == 404
    assert "404" in response.content.decode()
    assert "Вернуться на главную" in response.content.decode()
