# route-service/app/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class RouteStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"


@dataclass
class Route:
    """
    Агрегат Bounded Context «Управление маршрутами».
    Содержит только данные о маршруте: откуда, куда, даты, владелец.
    """
    owner_id: str
    title: str
    origin: str
    destination: str
    start_date: date
    end_date: date
    id: UUID = field(default_factory=uuid4)
    status: RouteStatus = RouteStatus.DRAFT
    description: Optional[str] = None

    def activate(self) -> None:
        self.status = RouteStatus.ACTIVE

    def complete(self) -> None:
        self.status = RouteStatus.COMPLETED
