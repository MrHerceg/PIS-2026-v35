from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from domain.models.route import Route
from domain.models.note import Note


@dataclass
class Trip:
    title: str
    start_date: date
    end_date: date
    budget: float
    routes: List[Route] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None

    def add_route(self, route: Route) -> None:
        self.routes.append(route)

    def add_note(self, note: Note) -> None:
        self.notes.append(note)

    def total_route_distance(self) -> float:
        return sum(r.distance_km for r in self.routes)

    def is_within_budget(self, spent: float) -> bool:
        return spent <= self.budget

    def __repr__(self) -> str:
        return (
            f"Trip(id={self.id}, title='{self.title}', "
            f"start={self.start_date}, end={self.end_date}, "
            f"budget={self.budget})"
        )
