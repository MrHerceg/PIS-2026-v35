from dataclasses import dataclass


@dataclass
class AddPlaceToRouteCommand:
    trip_id: str
    place_id: str
