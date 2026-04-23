# application/service/trip_service.py
from typing import List, Optional

from application.command.add_note_command import AddNoteCommand
from application.command.add_place_command import AddPlaceToRouteCommand
from application.command.create_trip_command import CreateTripCommand
from application.command.handlers.add_note_handler import AddNoteHandler
from application.command.handlers.add_place_handler import AddPlaceToRouteHandler
from application.command.handlers.create_trip_handler import CreateTripHandler
from application.ports import GeoService, NotificationService, TripRepository
from application.query.dto.trip_dto import TripDto
from application.query.get_trip_by_id_query import GetTripByIdQuery
from application.query.handlers.get_trip_by_id_handler import GetTripByIdHandler
from application.query.handlers.list_trips_handler import ListActiveTripsHandler, ListTripsByOwnerHandler
from application.query.list_trips_query import ListActiveTripsQuery, ListTripsByOwnerQuery


class TripService:
    """
    Фасад уровня приложения (Application Service).
    Маршрутизирует вызовы к Command/Query-обработчикам.
    """

    def __init__(
        self,
        repository: TripRepository,
        geo_service: Optional[GeoService],
        notification_service: NotificationService,
    ) -> None:
        self._create_handler     = CreateTripHandler(repository, notification_service)
        self._add_place_handler  = AddPlaceToRouteHandler(repository, geo_service)
        self._add_note_handler   = AddNoteHandler(repository)
        self._get_handler        = GetTripByIdHandler(repository)
        self._list_handler       = ListTripsByOwnerHandler(repository)
        self._active_handler     = ListActiveTripsHandler(repository)

    # ── Commands ──────────────────────────────────────────────────────────────

    def create_trip(
        self,
        owner_id: str,
        title: str,
        start_date,
        end_date,
        budget: float,
    ) -> str:
        cmd = CreateTripCommand(
            owner_id=owner_id,
            title=title,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
        )
        return self._create_handler.handle(cmd)

    def add_place_to_route(self, trip_id: str, place_id: str) -> None:
        cmd = AddPlaceToRouteCommand(trip_id=trip_id, place_id=place_id)
        self._add_place_handler.handle(cmd)

    def add_note(self, trip_id: str, text: str) -> str:
        cmd = AddNoteCommand(trip_id=trip_id, text=text)
        return self._add_note_handler.handle(cmd)

    # ── Queries ───────────────────────────────────────────────────────────────

    def get_trip_by_id(self, trip_id: str) -> Optional[TripDto]:
        return self._get_handler.handle(GetTripByIdQuery(trip_id=trip_id))

    def list_trips_by_owner(self, owner_id: str, status: Optional[str] = None) -> List[TripDto]:
        return self._list_handler.handle(ListTripsByOwnerQuery(owner_id=owner_id, status=status))

    def list_active_trips(self) -> List[TripDto]:
        return self._active_handler.handle(ListActiveTripsQuery())
