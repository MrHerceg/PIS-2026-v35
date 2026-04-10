from abc import ABC, abstractmethod

class NotificationService(ABC):
    """Исходящий порт для отправки уведомлений"""
    @abstractmethod
    def notify_trip_created(self, trip_id: str, owner_id: str) -> None: pass

    @abstractmethod
    def notify_budget_exceeded(self, trip_id: str, excess: float) -> None: pass
