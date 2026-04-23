# application/query/get_trip_by_id_query.py
from dataclasses import dataclass


@dataclass(frozen=True)
class GetTripByIdQuery:
    trip_id: str
