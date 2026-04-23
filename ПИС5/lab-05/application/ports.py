# application/ports.py
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.trip import Place, Trip


class TripRepository(ABC):
    @abstractmethod
    def save(self, trip: Trip) -> None: ...

    @abstractmethod
    def find_by_id(self, trip_id: str) -> Optional[Trip]: ...

    @abstractmethod
    def find_by_owner(self, owner_id: str) -> List[Trip]: ...

    @abstractmethod
    def find_active_trips(self) -> List[Trip]: ...


class GeoService(ABC):
    @abstractmethod
    def find_place(self, place_id: str) -> Optional[Place]: ...


class NotificationService(ABC):
    @abstractmethod
    def send_trip_created(self, owner_id: str, trip_id: str, title: str) -> None: ...


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event_type: str, payload: dict) -> None: ...
