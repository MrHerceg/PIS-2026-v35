# application/query/dto/trip_dto.py
from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class TripDto:
    """
    Упрощённая модель поездки для чтения (Read DTO).

    Поля:
        id         — уникальный идентификатор поездки
        owner_id   — идентификатор владельца
        title      — название поездки
        start_date — дата начала
        end_date   — дата окончания
        budget     — бюджет
        status     — текущий статус (draft / planned / in_progress / completed)
        route_ids  — список идентификаторов мест в маршруте
        notes      — список текстов заметок
    """
    id: str
    owner_id: str
    title: str
    start_date: date
    end_date: date
    budget: float
    status: str
    route_ids: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
