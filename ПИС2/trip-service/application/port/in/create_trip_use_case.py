from abc import ABC, abstractmethod
from datetime import date

class CreateTripCommand:
    """DTO для команды создания поездки"""
    def __init__(self, owner_id: str, title: str,
                 start_date: date, end_date: date, budget: float):
        self.owner_id   = owner_id
        self.title      = title
        self.start_date = start_date
        self.end_date   = end_date
        self.budget     = budget

class CreateTripUseCase(ABC):
    """Входящий порт для создания поездки"""
    @abstractmethod
    def create(self, command: CreateTripCommand) -> str:
        """Создаёт поездку и возвращает trip_id"""
        pass
