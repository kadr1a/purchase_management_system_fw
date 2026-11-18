"""SQL-запросы, используемые Django-представлениями."""

from db.database import get_connection


PRODUCT_LIST_SQL = """
SELECT id, name, price, description FROM products ORDER BY name
"""
PRODUCT_SEARCH_SQL = """
SELECT id, name, price, description FROM products
WHERE price >= ? ORDER BY price
"""
SUPPLIER_LIST_SQL = """
SELECT id, name, contact, rating FROM suppliers
ORDER BY rating DESC, name
"""
APPLICATION_LIST_SQL = """
SELECT a.id, a.purpose, a.status, COUNT(ai.id) AS item_count,
       COALESCE(SUM(p.price * ai.quantity), 0) AS application_total
FROM applications AS a
LEFT JOIN application_items AS ai ON ai.application_id = a.id
LEFT JOIN products AS p ON p.id = ai.product_id
GROUP BY a.id, a.purpose, a.status ORDER BY a.id
"""
ORDER_LIST_SQL = """
SELECT po.id, po.total, po.status, a.id AS application_id,
       a.purpose, s.name AS supplier_name, s.contact
FROM purchase_orders AS po
JOIN applications AS a ON a.id = po.application_id
JOIN suppliers AS s ON s.id = po.supplier_id
ORDER BY po.id
"""
STATISTICS_SQL = """
SELECT (SELECT COUNT(*) FROM products) AS products_count,
       (SELECT COUNT(*) FROM suppliers) AS suppliers_count,
       (SELECT COUNT(*) FROM applications) AS applications_count,
       (SELECT COUNT(*) FROM purchase_orders) AS orders_count,
       (SELECT COALESCE(SUM(total), 0) FROM purchase_orders
        WHERE status = 'Оформлен') AS active_order_total
"""


def fetch_all(query, parameters=()):
    """Выполняет SELECT и возвращает строки sqlite3.Row."""
    connection = get_connection()
    try:
        return connection.execute(query, parameters).fetchall()
    finally:
        connection.close()


def fetch_one(query, parameters=()):
    """Выполняет SELECT и возвращает одну строку или None."""
    connection = get_connection()
    try:
        return connection.execute(query, parameters).fetchone()
    finally:
        connection.close()
