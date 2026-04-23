# application/command/handlers/add_place_handler.py
import warnings

from application.command.add_place_command import AddPlaceToRouteCommand
from application.ports import GeoService, TripRepository


class AddPlaceToRouteHandler:
    COST_PER_PLACE = 50.0

    def __init__(self, repository: TripRepository, geo_service: GeoService) -> None:
        self._repo = repository
        self._geo  = geo_service

    def handle(self, command: AddPlaceToRouteCommand) -> None:
        trip = self._repo.find_by_id(command.trip_id)
        if trip is None:
            raise ValueError(f"Поездка с id={command.trip_id} не найдена")

        place = self._geo.find_place(command.place_id) if self._geo else None
        if place is None:
            raise ValueError(f"Место с id={command.place_id} не найдено")

        projected = (len(trip.route) + 1) * self.COST_PER_PLACE
        if projected > trip.budget:
            warnings.warn(
                f"Добавление '{place.name}' может превысить бюджет "
                f"(бюджет: {trip.budget}, расходы: {projected})",
                UserWarning, stacklevel=2,
            )

        trip.add_place(place)
        self._repo.save(trip)
