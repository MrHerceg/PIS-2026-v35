# application/ports.py
# Абстрактные порты (интерфейсы) для обработчиков команд и запросов
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.trip import Place, Trip


class TripRepository(ABC):
    """Порт исходящего адаптера: хранилище поездок."""

    @abstractmethod
    def save(self, trip: Trip) -> None: ...

    @abstractmethod
    def find_by_id(self, trip_id: str) -> Optional[Trip]: ...

    @abstractmethod
    def find_by_owner(self, owner_id: str) -> List[Trip]: ...

    @abstractmethod
    def find_all(self) -> List[Trip]: ...


class GeoService(ABC):
    """Порт исходящего адаптера: геосервис."""

    @abstractmethod
    def find_place(self, place_id: str) -> Optional[Place]: ...


class NotificationService(ABC):
    """Порт исходящего адаптера: уведомления."""

    @abstractmethod
    def send_trip_created(self, owner_id: str, trip_id: str, title: str) -> None: ...
