# application/command/create_trip_command.py
from dataclasses import dataclass
from datetime import date


@dataclass
class CreateTripCommand:
    owner_id:   str
    title:      str
    start_date: date
    end_date:   date
    budget:     float

    def __post_init__(self) -> None:
        if not self.owner_id:
            raise ValueError("owner_id обязательно")
        if not self.title:
            raise ValueError("title обязательно")
        if self.end_date <= self.start_date:
            raise ValueError("end_date должна быть позже start_date")
        if self.budget < 0:
            raise ValueError("budget должен быть ≥ 0")
