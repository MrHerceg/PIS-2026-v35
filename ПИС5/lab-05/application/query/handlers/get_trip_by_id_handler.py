# application/query/handlers/get_trip_by_id_handler.py
from typing import Optional

from application.ports import TripRepository
from application.query.dto.trip_dto import TripDto
from application.query.get_trip_by_id_query import GetTripByIdQuery
from domain.models.trip import Trip


def _to_dto(trip: Trip) -> TripDto:
    return TripDto(
        id=str(trip.id),
        owner_id=trip.owner_id,
        title=trip.title,
        start_date=trip.start_date,
        end_date=trip.end_date,
        budget=trip.budget,
        status=trip.status.value,
        route_ids=[p.place_id for p in trip.route],
        notes=[n.text for n in trip.notes],
    )


class GetTripByIdHandler:
    """
    Обработчик запроса GetTripByIdQuery.
    Репозиторий: TripRepository
    Возвращает: TripDto | None
    """

    def __init__(self, repository: TripRepository) -> None:
        self._repo = repository

    def handle(self, query: GetTripByIdQuery) -> Optional[TripDto]:
        trip = self._repo.find_by_id(query.trip_id)
        if trip is None:
            return None
        return _to_dto(trip)
