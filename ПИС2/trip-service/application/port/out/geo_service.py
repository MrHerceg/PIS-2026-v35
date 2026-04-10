from abc import ABC, abstractmethod
from typing import List

class GeoService(ABC):
    """Исходящий порт: поиск мест через внешний геосервис"""
    @abstractmethod
    def search_places(self, query: str) -> List[dict]: pass

    @abstractmethod
    def get_place_by_id(self, place_id: str) -> dict: pass
