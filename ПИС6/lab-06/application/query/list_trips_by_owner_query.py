from dataclasses import dataclass


@dataclass
class ListTripsByOwnerQuery:
    owner_id: str
