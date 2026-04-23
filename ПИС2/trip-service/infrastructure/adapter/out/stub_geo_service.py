import math

from application.port.out.geo_service import Coordinates, GeoService


# Stub coordinates for demo purposes
_COORDS: dict = {
    "минск": Coordinates(53.9045, 27.5615),
    "брест": Coordinates(52.0976, 23.7341),
    "гродно": Coordinates(53.6834, 23.8258),
    "витебск": Coordinates(55.1904, 30.2049),
    "гомель": Coordinates(52.4345, 30.9754),
    "могилёв": Coordinates(53.9168, 30.3449),
    "варшава": Coordinates(52.2297, 21.0122),
    "вильнюс": Coordinates(54.6872, 25.2797),
}


class StubGeoService(GeoService):
    """
    Outgoing adapter stub: returns hardcoded coordinates and distances.
    In production, replace with a real geocoding API (e.g. OpenStreetMap/Nominatim).
    """

    def get_coordinates(self, place_name: str) -> Coordinates:
        key = place_name.lower()
        if key in _COORDS:
            return _COORDS[key]
        # Default fallback
        return Coordinates(0.0, 0.0)

    def calculate_distance_km(self, origin: str, destination: str) -> float:
        c1 = self.get_coordinates(origin)
        c2 = self.get_coordinates(destination)
        return self._haversine(c1, c2)

    @staticmethod
    def _haversine(c1: Coordinates, c2: Coordinates) -> float:
        R = 6371.0
        lat1, lon1 = math.radians(c1.latitude), math.radians(c1.longitude)
        lat2, lon2 = math.radians(c2.latitude), math.radians(c2.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return R * 2 * math.asin(math.sqrt(a))
