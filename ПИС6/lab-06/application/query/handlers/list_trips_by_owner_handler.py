from typing import List
from application.query.list_trips_by_owner_query import ListTripsByOwnerQuery
from application.query.trip_dto import TripDto


class ListTripsByOwnerHandler:
    def __init__(self, repository):
        self._repo = repository

    def handle(self, query: ListTripsByOwnerQuery) -> List[TripDto]:
        trips = self._repo.find_by_owner(query.owner_id)
        return [
            TripDto(
                id=t.id,
                owner_id=t.owner_id,
                title=t.title,
                start_date=t.start_date,
                end_date=t.end_date,
                budget=t.budget,
                status=t.status,
                route_ids=list(t.route_ids),
                notes=list(t.notes),
            )
            for t in trips
        ]
