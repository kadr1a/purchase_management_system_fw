"""Общие утилиты для безопасного поиска по строковым полям ORM."""
from django.db.models import Q


def casefold_search(queryset, query, fields):
    """Ищет без учёта регистра, включая кириллицу в SQLite.

    SQLite LIKE не выполняет Unicode case-folding для кириллицы.
    Поэтому ORM-фильтр icontains дополняется списком совпавших PK,
    найденных через Python casefold().
    """
    if not query:
        return queryset
    normalized = query.casefold()
    rows = queryset.values_list("pk", *fields)
    matching_ids = [
        row[0] for row in rows
        if any(normalized in (value or "").casefold() for value in row[1:])
    ]
    conditions = Q(pk__in=matching_ids)
    for field in fields:
        conditions |= Q(**{f"{field}__icontains": query})
    return queryset.filter(conditions)


def casefold_exact_search(queryset, field, value):
    """Точное сравнение без учёта регистра, в том числе для кириллицы."""
    if not value:
        return queryset
    normalized = value.casefold()
    matching_ids = [
        row[0] for row in queryset.values_list("pk", field)
        if (row[1] or "").casefold() == normalized
    ]
    return queryset.filter(
        Q(**{f"{field}__iexact": value}) | Q(pk__in=matching_ids)
    )
