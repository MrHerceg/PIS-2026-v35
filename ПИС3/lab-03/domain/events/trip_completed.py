from dataclasses import dataclass
from datetime import datetime
from .base import DomainEvent


@dataclass
class TripCompleted(DomainEvent):
    trip_id: str = ""
    completed_at: datetime = None

    def __post_init__(self):
        super().__post_init__() if hasattr(super(), '__post_init__') else None
        if self.completed_at is None:
            self.completed_at = self.occurred_at

    def __repr__(self):
        return f"TripCompleted(trip_id={self.trip_id}, completed_at={self.completed_at})"
