# application/query/list_trips_query.py
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ListTripsByOwnerQuery:
    """
    Запрос для получения списка поездок пользователя с опциональной фильтрацией.

    Поля:
        owner_id — идентификатор владельца (обязательное)
        status   — фильтр по статусу (опционально):
                   "draft" | "planned" | "in_progress" | "completed"
    """
    owner_id: str
    status: Optional[str] = None
