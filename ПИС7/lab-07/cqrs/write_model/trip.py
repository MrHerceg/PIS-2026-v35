from datetime import date, datetime
from typing import List


class Trip:
    """Write Model: агрегат поездки"""

    def __init__(self, trip_id: str, owner_id: str, title: str,
                 start_date: date, end_date: date, budget: float):
        # Инварианты при создании
        if end_date <= start_date:
            raise ValueError("end_date must be after start_date")
        if budget < 0:
            raise ValueError("budget must be non-negative")

        self.id         = trip_id
        self.owner_id   = owner_id
        self.title      = title
        self.start_date = start_date
        self.end_date   = end_date
        self.budget     = budget
        self.status     = "PLANNED"
        self.route_ids: List[str] = []
        self.notes:     List[str] = []
        self.created_at = datetime.now()

    def add_place(self, place_id: str) -> None:
        """Бизнес-метод: добавить место в маршрут"""
        if self.status == "COMPLETED":
            raise ValueError("Cannot modify a completed trip")
        if place_id in self.route_ids:
            raise ValueError(f"Place {place_id} already in route")
        self.route_ids.append(place_id)

    def add_note(self, text: str) -> None:
        """Бизнес-метод: добавить заметку"""
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty")
        self.notes.append(text.strip())

    def complete(self) -> None:
        """Перевести поездку в статус COMPLETED"""
        if self.status == "COMPLETED":
            raise ValueError("Trip is already completed")
        self.status = "COMPLETED"
