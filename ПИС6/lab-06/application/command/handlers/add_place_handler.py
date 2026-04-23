from application.command.add_place_command import AddPlaceToRouteCommand


class AddPlaceToRouteHandler:
    def __init__(self, repository, geo_service=None):
        self._repo = repository
        self._geo = geo_service

    def handle(self, command: AddPlaceToRouteCommand) -> None:
        trip = self._repo.find_by_id(command.trip_id)
        if trip is None:
            raise ValueError(f"Trip '{command.trip_id}' not found")

        trip.add_place(command.place_id)
        self._repo.save(trip)
