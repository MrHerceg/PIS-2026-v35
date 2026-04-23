# application/query/list_trips_query.py
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ListTripsByOwnerQuery:
    owner_id: str
    status: Optional[str] = None


@dataclass(frozen=True)
class ListActiveTripsQuery:
    pass
