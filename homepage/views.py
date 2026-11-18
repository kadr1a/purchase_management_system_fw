"""Главная страница и общие элементы HTML-интерфейса."""
from django.http import HttpResponse
from django.utils.html import escape


def page(title, content):
    """Формирует общий HTML-каркас страниц с Bootstrap."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<link rel="stylesheet" href="{bootstrap}">
<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
<div class="container">
<a class="navbar-brand" href="/">Закупки</a>
<div class="navbar-nav">
<a class="nav-link" href="/">Главная</a>
<a class="nav-link" href="/products/">Товары</a>
<a class="nav-link" href="/suppliers/">Поставщики</a>
<a class="nav-link" href="/applications/">Заявки</a>
<a class="nav-link" href="/orders/">Заказы</a>
</div>
</div>
</nav>
<main class="container py-4">{content}</main>
<footer class="container pb-4 text-muted">
Система управления закупками · Практическая работа № 5
</footer>
</body>
</html>"""


def index(request):
    """Отображает главную страницу системы."""
    content = """
    <section class="p-5 mb-4 bg-light rounded-3">
      <h1 class="display-5">Система управления закупками</h1>
      <p class="lead">Учёт товаров, поставщиков, заявок и заказов организации.</p>
      <p>Выберите раздел для просмотра данных предметной области.</p>
    </section>
    <div class="row g-3">
      <div class="col-md-6 col-lg-3"><a class="section-card" href="/products/">
        <h2>Товары</h2><p>Каталог и цены товаров</p></a></div>
      <div class="col-md-6 col-lg-3"><a class="section-card" href="/suppliers/">
        <h2>Поставщики</h2><p>Контактная информация и рейтинг</p></a></div>
      <div class="col-md-6 col-lg-3"><a class="section-card" href="/applications/">
        <h2>Заявки</h2><p>Состав и статус заявок</p></a></div>
      <div class="col-md-6 col-lg-3"><a class="section-card" href="/orders/">
        <h2>Заказы</h2><p>Оформленные заказы поставщикам</p></a></div>
    </div>
    """
    return HttpResponse(page("Главная — Управление закупками", content))


def page_not_found(request, exception):
    """Возвращает оформленную страницу с HTTP-статусом 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Запрошенный адрес не существует.</p>
    <a href="/" class="btn btn-primary">Вернуться на главную</a>
    """
    return HttpResponse(page("404 — страница не найдена", content), status=404)
