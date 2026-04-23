from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4


class TripStatus(str, Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Place:
    place_id: str
    name: str
    latitude: float = 0.0
    longitude: float = 0.0


@dataclass
class Note:
    id: UUID = field(default_factory=uuid4)
    text: str = ""


@dataclass
class Trip:
    owner_id: str
    title: str
    start_date: date
    end_date: date
    budget: float
    id: UUID = field(default_factory=uuid4)
    status: TripStatus = TripStatus.DRAFT
    route: List[Place] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)
    description: Optional[str] = None

    def add_place(self, place: Place) -> None:
        self.route.append(place)

    def add_note(self, note: Note) -> None:
        self.notes.append(note)

    @property
    def route_ids(self) -> List[str]:
        return [p.place_id for p in self.route]
