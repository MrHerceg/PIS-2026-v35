# place-service/app/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Place:
    """
    Место посещения в рамках маршрута.
    Bounded Context: Управление местами и бюджетом.
    """
    route_id:   str
    name:       str
    latitude:   float = 0.0
    longitude:  float = 0.0
    visit_date: Optional[date] = None
    id: UUID = field(default_factory=uuid4)


@dataclass
class Budget:
    """Бюджет маршрута."""
    route_id: str
    amount:   float
    currency: str = "BYN"
    id: UUID = field(default_factory=uuid4)


@dataclass
class Note:
    """Заметка, привязанная к маршруту."""
    route_id: str
    text:     str
    id: UUID = field(default_factory=uuid4)
