from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Location:
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Location name cannot be empty")
        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValueError("Invalid latitude: must be between -90 and 90")
        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValueError("Invalid longitude: must be between -180 and 180")

    def __str__(self):
        if self.latitude is not None and self.longitude is not None:
            return f"{self.name} ({self.latitude}, {self.longitude})"
        return self.name
