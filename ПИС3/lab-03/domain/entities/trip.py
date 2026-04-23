import uuid
from datetime import datetime
from typing import List, Optional

from domain.value_objects.date_range import DateRange
from domain.value_objects.money import Money
from domain.value_objects.location import Location
from domain.entities.note import Note
from domain.events.trip_created import TripCreated
from domain.events.route_planned import RoutePlanned
from domain.events.trip_completed import TripCompleted
from domain.exceptions.domain_exceptions import (
    TripAlreadyCompletedException,
    InvalidRouteException,
)


class Trip:
    """Агрегатный корень. Управляет маршрутом, бюджетом и заметками поездки."""

    def __init__(self, name: str, date_range: DateRange):
        if not name or not name.strip():
            raise ValueError("Trip name cannot be empty")

        self.id: str = str(uuid.uuid4())
        self.name: str = name.strip()
        self.date_range: DateRange = date_range
        self.budget: Money = Money(0, "USD")
        self.route: Optional[List[Location]] = None
        self.notes: List[Note] = []
        self.completed: bool = False
        self.created_at: datetime = datetime.now()

        self._events: List = [TripCreated(trip_id=self.id, name=self.name)]

    # ------------------------------------------------------------------ #
    # Инварианты / бизнес-правила
    # ------------------------------------------------------------------ #

    def _ensure_not_completed(self):
        if self.completed:
            raise TripAlreadyCompletedException(self.id)

    # ------------------------------------------------------------------ #
    # Изменение маршрута
    # ------------------------------------------------------------------ #

    def add_route(self, locations: List[Location]) -> None:
        self._ensure_not_completed()
        if len(locations) < 2:
            raise InvalidRouteException("Route must have at least 2 locations")
        self.route = list(locations)
        self._events.append(
            RoutePlanned(trip_id=self.id, locations=[loc.name for loc in locations])
        )

    # ------------------------------------------------------------------ #
    # Бюджет
    # ------------------------------------------------------------------ #

    def change_budget(self, new_budget: Money) -> None:
        self._ensure_not_completed()
        self.budget = new_budget

    # ------------------------------------------------------------------ #
    # Заметки
    # ------------------------------------------------------------------ #

    def add_note(self, text: str) -> Note:
        self._ensure_not_completed()
        note = Note(text)
        self.notes.append(note)
        return note

    # ------------------------------------------------------------------ #
    # Завершение поездки
    # ------------------------------------------------------------------ #

    def complete(self) -> None:
        self._ensure_not_completed()
        self.completed = True
        self._events.append(TripCompleted(trip_id=self.id, completed_at=datetime.now()))

    # ------------------------------------------------------------------ #
    # События
    # ------------------------------------------------------------------ #

    def pull_events(self) -> List:
        """Извлекает и очищает накопленные доменные события."""
        events = list(self._events)
        self._events.clear()
        return events

    def __repr__(self):
        return (
            f"Trip(id={self.id!r}, name={self.name!r}, "
            f"completed={self.completed}, budget={self.budget})"
        )
