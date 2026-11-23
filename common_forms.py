"""Общие вспомогательные средства для форм проекта."""
import uuid


def make_record_id(prefix):
    """Создаёт короткий уникальный строковый идентификатор."""
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"
