import uuid
from datetime import date
from domain.models.trip import Trip
from application.command.create_trip_command import CreateTripCommand


class CreateTripHandler:
    def __init__(self, repository, notification_service=None):
        self._repo = repository
        self._notify = notification_service

    def handle(self, command: CreateTripCommand) -> str:
        trip_id = str(uuid.uuid4())
        trip = Trip(
            trip_id=trip_id,
            owner_id=command.owner_id,
            title=command.title,
            start_date=command.start_date,
            end_date=command.end_date,
            budget=command.budget,
        )
        self._repo.save(trip)

        if self._notify is not None:
            self._notify.notify_trip_created(trip_id, command.owner_id)

        return trip_id
