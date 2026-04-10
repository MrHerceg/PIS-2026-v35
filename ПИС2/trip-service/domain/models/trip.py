from datetime import date
from typing import List, Optional

class Trip:
    """Доменная модель: Поездка"""

    def __init__(self, trip_id: str, owner_id: str,
                 title: str, start_date: date, end_date: date,
                 budget: float):
        self.id          = trip_id
        self.owner_id    = owner_id
        self.title       = title
        self.start_date  = start_date
        self.end_date    = end_date
        self.budget      = budget
        self.status      = "PLANNED"
        self.route_ids: List[str] = []
        self.notes: List[str]     = []

    def add_place(self, place_id: str) -> None:
        """Бизнес-метод добавления места в маршрут"""
        if place_id not in self.route_ids:
            self.route_ids.append(place_id)

    def add_note(self, text: str) -> None:
        """Добавить заметку к поездке"""
        self.notes.append(text)

    def validate_dates(self) -> bool:
        """Проверка корректности дат"""
        return self.end_date > self.start_date
