from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class TripDto:
    id: str
    owner_id: str
    title: str
    start_date: date
    end_date: date
    budget: float
    status: str
    route_ids: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
