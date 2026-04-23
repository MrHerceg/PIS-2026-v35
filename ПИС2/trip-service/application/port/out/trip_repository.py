from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.trip import Trip


class TripRepository(ABC):
    """Outgoing port: persistence contract for trips."""

    @abstractmethod
    def save(self, trip: Trip) -> None:
        ...

    @abstractmethod
    def find_by_id(self, trip_id: str) -> Optional[Trip]:
        ...

    @abstractmethod
    def find_all(self) -> List[Trip]:
        ...

    @abstractmethod
    def delete(self, trip_id: str) -> bool:
        ...
