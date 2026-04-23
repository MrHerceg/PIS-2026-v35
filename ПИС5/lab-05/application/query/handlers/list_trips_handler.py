# application/query/handlers/list_trips_handler.py
from typing import List

from application.ports import TripRepository
from application.query.dto.trip_dto import TripDto
from application.query.list_trips_query import ListActiveTripsQuery, ListTripsByOwnerQuery
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


class ListTripsByOwnerHandler:
    """
    Обработчик запроса ListTripsByOwnerQuery.
    Репозиторий: TripRepository
    Возвращает: List[TripDto]
    """

    def __init__(self, repository: TripRepository) -> None:
        self._repo = repository

    def handle(self, query: ListTripsByOwnerQuery) -> List[TripDto]:
        trips = self._repo.find_by_owner(query.owner_id)
        if query.status is not None:
            trips = [t for t in trips if t.status.value == query.status]
        return [_to_dto(t) for t in trips]


class ListActiveTripsHandler:
    """
    Обработчик запроса ListActiveTripsQuery.
    Возвращает поездки со статусом, отличным от COMPLETED.
    """

    def __init__(self, repository: TripRepository) -> None:
        self._repo = repository

    def handle(self, query: ListActiveTripsQuery) -> List[TripDto]:
        trips = self._repo.find_active_trips()
        return [_to_dto(t) for t in trips]
