from abc import ABC, abstractmethod
from typing import Optional, List

class TripRepository(ABC):
    """Исходящий порт для работы с хранилищем поездок"""
    @abstractmethod
    def save(self, trip) -> None: pass

    @abstractmethod
    def find_by_id(self, trip_id: str) -> Optional[object]: pass

    @abstractmethod
    def find_by_owner(self, owner_id: str) -> List[object]: pass
