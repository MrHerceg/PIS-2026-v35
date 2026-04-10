from dataclasses import dataclass

@dataclass(frozen=True)
class Place:
    """Value Object: Место на маршруте"""
    place_id:    str
    name:        str
    country:     str
    latitude:    float
    longitude:   float
    est_cost:    float  # Оценочная стоимость посещения
