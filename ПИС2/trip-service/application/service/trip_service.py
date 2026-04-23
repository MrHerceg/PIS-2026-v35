from typing import List, Optional

from application.port.in_.create_trip_use_case import CreateTripCommand, CreateTripUseCase
from application.port.in_.get_trip_use_case import GetTripUseCase
from application.port.out.trip_repository import TripRepository
from application.port.out.geo_service import GeoService
from application.port.out.notification_service import NotificationService
from domain.models.trip import Trip


class TripService(CreateTripUseCase, GetTripUseCase):
    """
    Application service that implements the incoming use case ports.
    It coordinates the domain logic and delegates to outgoing ports.
    """

    def __init__(
        self,
        trip_repository: TripRepository,
        geo_service: GeoService,
        notification_service: NotificationService,
    ) -> None:
        self._repo = trip_repository
        self._geo = geo_service
        self._notifier = notification_service

    # --- CreateTripUseCase ---

    def create_trip(self, command: CreateTripCommand) -> str:
        trip = Trip(
            title=command.title,
            start_date=command.start_date,
            end_date=command.end_date,
            budget=command.budget,
            description=command.description,
        )
        self._repo.save(trip)
        return str(trip.id)

    # --- GetTripUseCase ---

    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        return self._repo.find_by_id(trip_id)

    def get_all_trips(self) -> List[Trip]:
        return self._repo.find_all()
