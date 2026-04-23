from abc import ABC, abstractmethod

from domain.models.trip import Trip


class NotificationService(ABC):
    """Outgoing port: contract for sending notifications."""

    @abstractmethod
    def notify_trip_created(self, trip: Trip, recipient_email: str) -> None:
        """Sends a notification when a new trip is created."""
        ...

    @abstractmethod
    def notify_trip_reminder(self, trip: Trip, recipient_email: str) -> None:
        """Sends a reminder notification for an upcoming trip."""
        ...
