from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Coordinates:
    latitude: float
    longitude: float


class GeoService(ABC):
    """Outgoing port: contract for geo/location operations."""

    @abstractmethod
    def get_coordinates(self, place_name: str) -> Coordinates:
        """Returns coordinates for a given place name."""
        ...

    @abstractmethod
    def calculate_distance_km(self, origin: str, destination: str) -> float:
        """Calculates the distance in km between two places."""
        ...
