# application/command/add_place_command.py
from dataclasses import dataclass


@dataclass
class AddPlaceToRouteCommand:
    trip_id:  str
    place_id: str

    def __post_init__(self) -> None:
        if not self.trip_id:
            raise ValueError("trip_id обязательно")
        if not self.place_id:
            raise ValueError("place_id обязательно")
