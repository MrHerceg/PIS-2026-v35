from dataclasses import dataclass
from datetime import datetime
from .base import DomainEvent


@dataclass
class TripCreated(DomainEvent):
    trip_id: str = ""
    name: str = ""

    def __repr__(self):
        return f"TripCreated(trip_id={self.trip_id}, name={self.name!r}, at={self.occurred_at})"
