from typing import Dict, List, Optional

from application.port.out.trip_repository import TripRepository
from domain.models.trip import Trip


class InMemoryTripRepository(TripRepository):
    """
    Outgoing adapter: stores trips in a plain Python dict.
    No database connection required — ideal for testing and prototyping.
    """

    def __init__(self) -> None:
        self._storage: Dict[str, Trip] = {}

    def save(self, trip: Trip) -> None:
        self._storage[str(trip.id)] = trip

    def find_by_id(self, trip_id: str) -> Optional[Trip]:
        return self._storage.get(trip_id)

    def find_all(self) -> List[Trip]:
        return list(self._storage.values())

    def delete(self, trip_id: str) -> bool:
        if trip_id in self._storage:
            del self._storage[trip_id]
            return True
        return False
