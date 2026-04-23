# infrastructure/repository/in_memory_trip_repository.py
from typing import Dict, List, Optional

from application.ports import TripRepository
from domain.models.trip import Trip


class InMemoryTripRepository(TripRepository):
    """
    Реализация TripRepository на основе словаря Python.
    Не требует подключения к БД — подходит для тестов и демонстрации.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Trip] = {}

    def save(self, trip: Trip) -> None:
        self._store[str(trip.id)] = trip

    def find_by_id(self, trip_id: str) -> Optional[Trip]:
        return self._store.get(trip_id)

    def find_by_owner(self, owner_id: str) -> List[Trip]:
        return [t for t in self._store.values() if t.owner_id == owner_id]

    def find_all(self) -> List[Trip]:
        return list(self._store.values())
