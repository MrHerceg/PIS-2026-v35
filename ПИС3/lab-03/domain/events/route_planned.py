from dataclasses import dataclass, field
from typing import List
from .base import DomainEvent


@dataclass
class RoutePlanned(DomainEvent):
    trip_id: str = ""
    locations: List[str] = field(default_factory=list)

    def __repr__(self):
        return f"RoutePlanned(trip_id={self.trip_id}, locations={self.locations})"
