from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Trip:
    trip_id: str
    owner_id: str
    title: str
    start_date: date
    end_date: date
    budget: float
    status: str = "PLANNED"
    route_ids: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    # Свойство-алиас для совместимости (handler-ы используют .id)
    @property
    def id(self) -> str:
        return self.trip_id

    def validate_dates(self) -> bool:
        """Возвращает True если start_date <= end_date."""
        return self.start_date <= self.end_date

    def add_place(self, place_id: str) -> None:
        """Добавляет место в маршрут (без дублей)."""
        if place_id not in self.route_ids:
            self.route_ids.append(place_id)

    def add_note(self, text: str) -> None:
        """Добавляет заметку к поездке."""
        self.notes.append(text)

    def complete(self) -> None:
        """Помечает поездку как завершённую."""
        self.status = "COMPLETED"

    def __repr__(self) -> str:
        return (
            f"Trip(id={self.trip_id!r}, title={self.title!r}, "
            f"status={self.status!r})"
        )
