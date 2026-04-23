from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Route:
    origin: str
    destination: str
    distance_km: float
    transport: str  # e.g. "car", "train", "plane", "bus"
    id: UUID = field(default_factory=uuid4)

    def __repr__(self) -> str:
        return (
            f"Route(id={self.id}, {self.origin} -> {self.destination}, "
            f"{self.distance_km} km, {self.transport})"
        )
