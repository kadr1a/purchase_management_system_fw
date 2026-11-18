# Система управления закупками

Индивидуальный проект по дисциплине «Технологии разработки приложений на базе фреймворков». Проект продолжает предыдущие практические работы: консольная версия и исходные JSON/SQL-данные сохранены, веб-интерфейс переведён на Django ORM (ПР9).

## Предметная область и возможности

- каталог товаров с ценами и описаниями;
- поставщики с контактами и рейтингом;
- заявки на закупку со списком товаров и количеством;
- заказы поставщикам, связанные с заявками и поставщиками;
- карточки сущностей, поиск, фильтрация и сортировка;
- статистика по количеству сущностей, суммам заказов и ценам товаров;
- административный CRUD через Django Admin.

## Стек

- Python 3.12+;
- Django 5.2;
- SQLite через Django ORM;
- pytest, pytest-django, flake8;
- Bootstrap 5.

## Модели и связи

| Django-модель | Поля | Связи |
|---|---|---|
| `Product` (`products_web`) | строковый PK `id`, `name`, `price`, `description` | товар используется в позициях заявок |
| `Supplier` (`suppliers_web`) | строковый PK `id`, `name`, `contact`, `rating` | один поставщик связан со многими заказами |
| `Application` (`applications_web`) | строковый PK `id`, `purpose`, `status` | заявка содержит позиции товаров |
| `ApplicationItem` (`applications_web`) | `application`, `product`, `quantity` | `ForeignKey` на заявку (`CASCADE`) и товар (`PROTECT`) |
| `PurchaseOrder` (`orders_web`) | строковый PK `id`, `application`, `supplier`, `total`, `status` | `OneToOneField` на заявку (`PROTECT`), `ForeignKey` на поставщика (`PROTECT`) |

Для связей заданы `related_name`: `Application.items`, `Product.application_items`, `Supplier.purchase_orders`, `Application.purchase_order`. Строковые первичные ключи сохраняют идентификаторы прежней системы. Для цены, рейтинга, количества и суммы добавлены ограничения целостности.

## ORM в представлениях

Представления больше не импортируют `db.repository` и не выполняют SQL-запросы. Используются:

- `all()`, `filter()`, `exclude()`, `get_object_or_404()` / `get()`;
- фильтры `icontains`, `istartswith`, `iexact`, числовые сравнения;
- поиск по нескольким полям и полям связанных моделей;
- `order_by()` с белыми списками разрешённых полей;
- `values()`, `annotate()`, `aggregate()`;
- `Count`, `Sum`, `Avg`, `Min`, `Max`;
- `select_related()` и `prefetch_related()`;
- `Paginator` с сохранением GET-параметров в навигации.

SQLite по умолчанию не выполняет Unicode case-folding для кириллицы в `LIKE`. В `orm_utils.py` добавлена небольшая совместимая функция поиска: ORM `icontains` дополняется поиском Python `casefold()`, поэтому поиск на русском не зависит от регистра. Параметры сортировки ограничены белым списком; некорректные значения фильтров не приводят к падению страницы.

## Страницы

| URL | Назначение |
|---|---|
| `/` | главная страница и сводные показатели |
| `/products/` | каталог, поиск, фильтр по минимальной цене, сортировка, пагинация |
| `/products/<id>/` | карточка товара |
| `/suppliers/` | поставщики, поиск и фильтр по рейтингу |
| `/suppliers/<id>/` | карточка поставщика |
| `/applications/` | заявки, поиск, фильтр по статусу, исключение статуса, сортировка, пагинация |
| `/applications/<id>/` | заявка и её товарные позиции |
| `/orders/` | заказы, поиск по заказу/заявке/поставщику, фильтр по статусу, пагинация |
| `/orders/<id>/` | карточка заказа |
| `/statistics/` | агрегированная статистика |

Несуществующие объекты возвращают 404. Невалидные параметры поиска/фильтрации обрабатываются без аварийного завершения.

## Структура проекта

- `procurement/` — настройки и корневые URL Django;
- `homepage/` — главная страница и статистика;
- `products_web/`, `suppliers_web/`, `applications_web/`, `orders_web/` — модели, миграции, представления, маршруты и шаблоны разделов;
- `templates/` — базовый шаблон, навигация и 404;
- `db/` — исходные SQL-модули ПР7 и скрипты инспекции/переноса данных;
- `models/`, `storage.py`, `main.py` — предметные классы и консольная версия предыдущих работ;
- `data/` — исходные JSON и SQLite ПР7;
- `sql/` — исходная SQL-схема и запросы ПР7;
- `tests/` — тесты предметной области и Django ORM.

## Установка и запуск

Из корня проекта:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py migrate
```

### Перенос данных ПР7

Перед переносом можно посмотреть структуру и количество записей исходной SQLite:

```bash
python db/inspect_source_db.py
```

Перенос из `data/procurement.sqlite3` в новую БД Django (`db.sqlite3`):

```bash
python db/import_sqlite_to_orm.py
```

Исходная база ПР7 не изменяется. Перенос выполняется в транзакции, использует `update_or_create()` по прежним ID и допускает повторный запуск. Альтернативный импорт из исходных JSON-файлов:

```bash
python db/import_json_to_orm.py
```

Проверка данных:

```bash
python manage.py shell
```

```python
from products_web.models import Product
from suppliers_web.models import Supplier
from applications_web.models import Application, ApplicationItem
from orders_web.models import PurchaseOrder

print(Product.objects.count(), Supplier.objects.count())
print(Application.objects.count(), ApplicationItem.objects.count())
print(PurchaseOrder.objects.count())
```

Запуск сервера:

```bash
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`. Для CRUD откройте `/admin/` и войдите под созданным суперпользователем (`python manage.py createsuperuser`).

## Проверки

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py showmigrations
pytest -v
flake8 . --extend-exclude=venv,.venv
```

Тесты покрывают связи и обратные связи, поиск, фильтрацию, агрегаты, карточки, 404, отмену заказа и прежние функции проекта.

## Важные замечания

- Миграции находятся в `*/migrations/` и должны храниться в Git.
- `db.sqlite3` — локальная ORM-база, не добавлять её в Git.
- `data/procurement.sqlite3`, SQL-схема и JSON сохранены как исходные данные предыдущих практических работ.
- Старые `db/database.py` и `db/repository.py` оставлены для демонстрации ПР7; веб-представления их больше не используют.
- Консольное приложение и доменные классы не удалены.

## Git

Коммиты этой практической работы начинаются с `PR9:`:

```bash
git add .
git commit -m "PR9: переход на Django ORM"
git push
```
