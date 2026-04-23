from typing import Optional
from application.query.get_trip_by_id_query import GetTripByIdQuery
from application.query.trip_dto import TripDto


class GetTripByIdHandler:
    def __init__(self, repository):
        self._repo = repository

    def handle(self, query: GetTripByIdQuery) -> Optional[TripDto]:
        trip = self._repo.find_by_id(query.trip_id)
        if trip is None:
            return None
        return TripDto(
            id=trip.id,
            owner_id=trip.owner_id,
            title=trip.title,
            start_date=trip.start_date,
            end_date=trip.end_date,
            budget=trip.budget,
            status=trip.status,
            route_ids=list(trip.route_ids),
            notes=list(trip.notes),
        )
