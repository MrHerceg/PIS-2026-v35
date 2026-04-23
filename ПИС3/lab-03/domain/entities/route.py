import uuid
from typing import List
from domain.value_objects.location import Location
from domain.exceptions.domain_exceptions import InvalidRouteException


class Route:
    def __init__(self, locations: List[Location]):
        if len(locations) < 2:
            raise InvalidRouteException("Route must have at least 2 locations")
        self.id: str = str(uuid.uuid4())
        self.locations: List[Location] = list(locations)

    def add_location(self, location: Location) -> None:
        self.locations.append(location)

    def remove_location(self, index: int) -> None:
        if len(self.locations) <= 2:
            raise InvalidRouteException("Cannot remove location: route must have at least 2 locations")
        self.locations.pop(index)

    def reorder(self, new_order: List[int]) -> None:
        if sorted(new_order) != list(range(len(self.locations))):
            raise InvalidRouteException("Invalid order indices")
        self.locations = [self.locations[i] for i in new_order]

    def __repr__(self):
        names = " → ".join(loc.name for loc in self.locations)
        return f"Route(id={self.id!r}, path={names!r})"
