from application.port.out.trip_repository import TripRepository

class InMemoryTripRepository(TripRepository):
    """Реализация TripRepository: хранение поездок в памяти"""

    def __init__(self):
        self.trips = {}  # Dict[str, Trip]

    def save(self, trip) -> None:
        """Сохраняет объект поездки в словарь"""
        self.trips[trip.id] = trip
        print(f"[DB] Поездка {trip.id} сохранена.")

    def find_by_id(self, trip_id: str):
        return self.trips.get(trip_id, None)

    def find_by_owner(self, owner_id: str):
        return [t for t in self.trips.values()
                if t.owner_id == owner_id]
