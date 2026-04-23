# infrastructure/repository/stub_geo_service.py
from typing import Optional

from application.ports import GeoService
from domain.models.trip import Place

_PLACES = {
    "place_minsk":    Place(place_id="place_minsk",    name="Минск",    latitude=53.9045, longitude=27.5615),
    "place_brest":    Place(place_id="place_brest",    name="Брест",    latitude=52.0976, longitude=23.7341),
    "place_grodno":   Place(place_id="place_grodno",   name="Гродно",   latitude=53.6834, longitude=23.8258),
    "place_vitebsk":  Place(place_id="place_vitebsk",  name="Витебск",  latitude=55.1904, longitude=30.2049),
    "place_warsaw":   Place(place_id="place_warsaw",   name="Варшава",  latitude=52.2297, longitude=21.0122),
    "place_vilnius":  Place(place_id="place_vilnius",  name="Вильнюс",  latitude=54.6872, longitude=25.2797),
}


class StubGeoService(GeoService):
    """Заглушка геосервиса для демонстрации и тестов."""

    def find_place(self, place_id: str) -> Optional[Place]:
        return _PLACES.get(place_id)
