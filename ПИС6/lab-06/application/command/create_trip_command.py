from dataclasses import dataclass
from datetime import date


@dataclass
class CreateTripCommand:
    owner_id: str
    title: str
    start_date: date
    end_date: date
    budget: float
