from dataclasses import dataclass


@dataclass
class GetTripByIdQuery:
    trip_id: str
