from abc import ABC, abstractmethod

class GetTripUseCase(ABC):
    """Входящий порт для получения поездки"""
    @abstractmethod
    def get_by_id(self, trip_id: str):
        """Возвращает поездку по идентификатору"""
        pass
