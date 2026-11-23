# Система управления закупками

Индивидуальный проект по дисциплине «Технологии разработки приложений на базе фреймворков». Проект продолжает предыдущие практические работы: консольная версия и исходные JSON/SQL-данные сохранены, веб-интерфейс переведён на Django ORM (ПР9), а в ПР10 настроена административная панель и расширены возможности ORM.

## Предметная область и возможности

- каталог товаров с ценами и описаниями;
- поставщики с контактами и рейтингом;
- заявки на закупку со списком товаров и количеством;
- заказы поставщикам, связанные с заявками и поставщиками;
- карточки сущностей, поиск, фильтрация и сортировка;
- статистика по количеству сущностей, суммам заказов и ценам товаров;
- административный CRUD через Django Admin: поиск, фильтры, сортировка, редактирование в списке, inline-связи и массовая отмена заказов;
- русскоязычная админ-панель с группировкой приложений и понятными названиями полей;
- карточки товаров с уникальными латинскими slug-адресами;
- снимок цены товара в позиции заявки и вычисляемая базой данных сумма `line_total`;
- общий контекстный процессор с количеством товаров, поставщиков, заявок и заказов;
- Django Debug Toolbar для анализа SQL в режиме разработки (подключается при установленной зависимости).

## Стек

- Python 3.12+;
- Django 5.2;
- SQLite через Django ORM (для `GeneratedField` требуется SQLite 3.31 или новее);
- pytest, pytest-django, flake8;
- Bootstrap 5;
- Django Debug Toolbar (разработка и анализ SQL).

## Модели и связи

| Django-модель | Поля | Связи |
|---|---|---|
| `Product` (`products_web`) | строковый PK `id`, `name`, уникальный `slug`, `price`, `description` | товар используется в позициях заявок; `get_absolute_url()` строит URL по slug |
| `Supplier` (`suppliers_web`) | строковый PK `id`, `name`, `contact`, `rating` | один поставщик связан со многими заказами |
| `Application` (`applications_web`) | строковый PK `id`, `purpose`, `status` (`TextChoices`) | заявка содержит позиции товаров |
| `ApplicationItem` (`applications_web`) | `application`, `product`, `quantity`, `unit_price`, вычисляемое `line_total` | `ForeignKey` на заявку (`CASCADE`) и товар (`PROTECT`); цена фиксируется на момент добавления, сумма рассчитывается `GeneratedField` на стороне БД |
| `PurchaseOrder` (`orders_web`) | строковый PK `id`, `application`, `supplier`, `total`, `status` (`TextChoices`) | `OneToOneField` на заявку (`PROTECT`), `ForeignKey` на поставщика (`PROTECT`) |

Для связей заданы `related_name`: `Application.items`, `Product.application_items`, `Supplier.purchase_orders`, `Application.purchase_order`. Строковые первичные ключи сохраняют идентификаторы прежней системы. Для цены, рейтинга, количества и суммы добавлены ограничения целостности.

## ORM в представлениях

Представления больше не импортируют `db.repository` и не выполняют SQL-запросы. Используются:

- `all()`, `filter()`, `exclude()`, `get_object_or_404()` / `get()`, логические `Q`-условия;
- фильтры `icontains`, `istartswith`, `iexact`, числовые сравнения;
- поиск по нескольким полям и полям связанных моделей;
- `order_by()` с белыми списками разрешённых полей;
- `values()`, `annotate()`, `aggregate()`, пользовательские `ApplicationQuerySet.with_summary()` / `ApplicationManager` и `PurchaseOrderQuerySet.ordered()` / `.cancelled()`;
- `Count`, `Sum`, `Avg`, `Min`, `Max`;
- `select_related()` и `prefetch_related()`;
- `Paginator` с сохранением GET-параметров в навигации.

SQLite по умолчанию не выполняет Unicode case-folding для кириллицы в `LIKE`. В `orm_utils.py` добавлена небольшая совместимая функция поиска: ORM `icontains` дополняется поиском Python `casefold()`, поэтому поиск на русском не зависит от регистра. Параметры сортировки ограничены белым списком; некорректные значения фильтров не приводят к падению страницы.

## Страницы

| URL | Назначение |
|---|---|
| `/` | главная страница и сводные показатели |
| `/products/` | каталог, поиск, фильтр по минимальной цене, сортировка, пагинация |
| `/products/<id>/` | совместимый маршрут карточки товара по ID |
| `/products/slug/<slug>/` | карточка товара по уникальному латинскому slug |
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

## Административная панель

Откройте `/admin/` и войдите под суперпользователем. Модели `Product`, `Supplier`, `Application` и `PurchaseOrder` зарегистрированы в админке. Для заявок настроено inline-редактирование позиций; в карточках поставщиков отображаются связанные заказы, а в карточках товаров — позиции заявок. Списки содержат столбцы, поиск, фильтры, сортировку и постраничный вывод. В списке заказов доступно массовое действие отмены оформленных заказов.

Создать администратора (один раз):

```bash
python manage.py createsuperuser
```

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

## Дополнительные возможности PR10

- `ApplicationItem.unit_price` хранит цену товара на момент включения в заявку; изменение текущей цены товара не меняет уже сформированную заявку.
- Статусы заявок и заказов заданы через `TextChoices`, а повторно используемые выборки вынесены в пользовательские `QuerySet` и менеджеры.
- `ApplicationItem.line_total` — `GeneratedField`, вычисляемый SQLite как произведение `unit_price` на `quantity`.
- `Product.slug` создаётся автоматически с транслитерацией русских названий, уникализируется суффиксом и используется в `get_absolute_url()`. Старый URL по ID сохранён для совместимости.
- `homepage.context_processors.procurement_context` передаёт общие счётчики в навигацию.
- Django Debug Toolbar добавляется в `INSTALLED_APPS`, middleware и URL только если пакет установлен и включён `DEBUG`. Зависимость включена в `requirements.txt`; после `pip install -r requirements.txt` панель доступна по `/__debug__/` на локальном адресе.

## Проверки

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py showmigrations
pytest -v
flake8 . --extend-exclude=venv,.venv
```

Тесты покрывают связи и обратные связи, поиск, фильтрацию, агрегаты, карточки, 404, отмену заказа, админ-регистрацию, slug, контекстный процессор и вычисляемую сумму позиции заявки.

## Важные замечания

- Миграции находятся в `*/migrations/` и должны храниться в Git.
- `db.sqlite3` — локальная ORM-база, не добавлять её в Git.
- `data/procurement.sqlite3`, SQL-схема и JSON сохранены как исходные данные предыдущих практических работ.
- Старые `db/database.py` и `db/repository.py` оставлены для демонстрации ПР7; веб-представления их больше не используют.
- Консольное приложение и доменные классы не удалены.

## Git

Коммит этой практической работы: `PR10: настройка Django Admin и расширение ORM`.

```bash
git status
git diff
git add .
git commit -m "PR10: настройка Django Admin и расширение ORM"
git push
```
