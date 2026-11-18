-- 1. Список всех товаров (SELECT, ORDER BY).
SELECT id, name, price, description
FROM products
ORDER BY name;

-- 2. Поиск товаров по минимальной цене (WHERE, параметр min_price).
SELECT id, name, price, description
FROM products
WHERE price >= ?
ORDER BY price;

-- 3. Список поставщиков с сортировкой по рейтингу.
SELECT id, name, contact, rating
FROM suppliers
ORDER BY rating DESC, name;

-- 4. Поставщики с рейтингом не ниже заданного (WHERE).
SELECT id, name, contact, rating
FROM suppliers
WHERE rating >= ?
ORDER BY rating DESC;

-- 5. Заявки и количество товарных позиций (LEFT JOIN, GROUP BY).
SELECT a.id, a.purpose, a.status, COUNT(ai.id) AS item_count
FROM applications AS a
LEFT JOIN application_items AS ai ON ai.application_id = a.id
GROUP BY a.id, a.purpose, a.status
ORDER BY a.id;

-- 6. Состав заявки с информацией о товарах (JOIN).
SELECT ai.application_id, p.id AS product_id, p.name AS product_name,
       p.price, ai.quantity, p.price * ai.quantity AS line_total
FROM application_items AS ai
JOIN products AS p ON p.id = ai.product_id
WHERE ai.application_id = ?
ORDER BY p.name;

-- 7. Полная информация о заказах (JOIN трёх таблиц).
SELECT po.id, po.total, po.status, a.id AS application_id,
       a.purpose, s.name AS supplier_name, s.contact
FROM purchase_orders AS po
JOIN applications AS a ON a.id = po.application_id
JOIN suppliers AS s ON s.id = po.supplier_id
ORDER BY po.id;

-- 8. Подсчёт количества записей по основным сущностям (COUNT).
SELECT (SELECT COUNT(*) FROM products) AS products_count,
       (SELECT COUNT(*) FROM suppliers) AS suppliers_count,
       (SELECT COUNT(*) FROM applications) AS applications_count,
       (SELECT COUNT(*) FROM purchase_orders) AS orders_count;

-- 9. Количество товарных позиций в заявках (GROUP BY, COUNT).
SELECT a.id, a.purpose, COUNT(ai.id) AS item_count
FROM applications AS a
LEFT JOIN application_items AS ai ON ai.application_id = a.id
GROUP BY a.id, a.purpose
ORDER BY item_count DESC, a.id;

-- 10. Заявки с количеством товарных позиций выше порога (HAVING).
SELECT a.id, a.purpose, COUNT(ai.id) AS item_count
FROM applications AS a
JOIN application_items AS ai ON ai.application_id = a.id
GROUP BY a.id, a.purpose
HAVING COUNT(ai.id) > ?
ORDER BY item_count DESC;

-- 11. Суммарная стоимость товарных позиций по заявкам (SUM, GROUP BY).
SELECT a.id, a.purpose,
       COALESCE(SUM(p.price * ai.quantity), 0) AS application_total
FROM applications AS a
LEFT JOIN application_items AS ai ON ai.application_id = a.id
LEFT JOIN products AS p ON p.id = ai.product_id
GROUP BY a.id, a.purpose
ORDER BY application_total DESC;

-- 12. Заказы по выбранному статусу (WHERE, параметр status).
SELECT id, application_id, supplier_id, total, status
FROM purchase_orders
WHERE status = ?
ORDER BY total DESC;
