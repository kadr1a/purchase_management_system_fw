"""Проверки шаблонного веб-интерфейса Django."""
import pytest
from django.test import Client, override_settings
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_main_page_uses_base_template_and_navigation():
    response = Client().get(reverse("homepage:index"))
    html = response.content.decode()
    assert response.status_code == 200
    assert "Система управления закупками" in html
    assert "Товары" in html
    assert "Поставщики" in html
    assert "/static/homepage/css/style.css" in html


@pytest.mark.parametrize(
    "route_name, heading",
    [
        ("products:list", "Товары"),
        ("suppliers:list", "Поставщики"),
        ("applications:list", "Заявки на закупку"),
        ("orders:list", "Заказы поставщикам"),
    ],
)
def test_section_pages_render(route_name, heading):
    response = Client().get(reverse(route_name))
    assert response.status_code == 200
    assert heading in response.content.decode()


@pytest.mark.parametrize(
    "url",
    [
        "/products/UNKNOWN/",
        "/suppliers/UNKNOWN/",
        "/applications/UNKNOWN/",
        "/orders/UNKNOWN/",
    ],
)
def test_missing_entities_return_404(url):
    response = Client().get(url)
    assert response.status_code == 404
    assert "не найден" in response.content.decode().lower()


@override_settings(DEBUG=False)
def test_custom_404_page():
    response = Client().get("/this-page-does-not-exist/")
    assert response.status_code == 404
    assert "Страница не найдена" in response.content.decode()
    assert "Вернуться на главную" in response.content.decode()
