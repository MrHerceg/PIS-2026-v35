from typing import Dict, List, Optional, Union
from domain.models.trip import Trip


class InMemoryTripRepository:
    """Лёгкий in-memory репозиторий — используется в E2E-тестах."""

    def __init__(self):
        self._store: Dict[str, Trip] = {}

    def save(self, trip: Union[Trip, dict]) -> None:
        if isinstance(trip, dict):
            from datetime import date as _date
            t = Trip(
                trip_id=trip["id"],
                owner_id=trip["owner_id"],
                title=trip["title"],
                start_date=trip["start_date"],
                end_date=trip["end_date"],
                budget=trip["budget"],
                status=trip.get("status", "PLANNED"),
            )
            t.route_ids = trip.get("route_ids", [])
            t.notes = trip.get("notes", [])
            self._store[t.trip_id] = t
        else:
            self._store[trip.trip_id] = trip

    def find_by_id(self, trip_id: str) -> Optional[Trip]:
        return self._store.get(trip_id)

    def find_by_owner(self, owner_id: str) -> List[Trip]:
        return [t for t in self._store.values() if t.owner_id == owner_id]

    def find_active_trips(self) -> List[Trip]:
        return [t for t in self._store.values() if t.status != "COMPLETED"]
