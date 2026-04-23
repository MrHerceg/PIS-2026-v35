from dataclasses import dataclass


@dataclass(frozen=True)
class Place:
    """Value Object — описывает географическое место в маршруте."""

    place_id: str
    name: str
    country: str
    latitude: float
    longitude: float
    est_cost: float = 0.0

    def __repr__(self) -> str:
        return f"Place(id={self.place_id!r}, name={self.name!r}, country={self.country!r})"
