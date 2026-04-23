from datetime import date
from typing import Any, Dict, List, Optional

from application.port.in_.create_trip_use_case import CreateTripCommand, CreateTripUseCase
from application.port.in_.get_trip_use_case import GetTripUseCase
from domain.models.trip import Trip


class TripController:
    """
    Incoming adapter: simulates a REST controller.
    In production, this would be wired to a framework such as FastAPI or Flask.
    Each method maps to an HTTP endpoint.
    """

    def __init__(
        self,
        create_trip_use_case: CreateTripUseCase,
        get_trip_use_case: GetTripUseCase,
    ) -> None:
        self._create = create_trip_use_case
        self._get = get_trip_use_case

    # POST /trips
    def handle_create_trip(self, body: Dict[str, Any]) -> Dict[str, str]:
        """
        Accepts a JSON-like dict and creates a new trip.

        Expected body keys:
            title (str), start_date (str ISO), end_date (str ISO),
            budget (float), description (str, optional)
        """
        command = CreateTripCommand(
            title=body["title"],
            start_date=date.fromisoformat(body["start_date"]),
            end_date=date.fromisoformat(body["end_date"]),
            budget=float(body["budget"]),
            description=body.get("description", ""),
        )
        trip_id = self._create.create_trip(command)
        return {"id": trip_id, "status": "created"}

    # GET /trips/<trip_id>
    def handle_get_trip(self, trip_id: str) -> Optional[Dict[str, Any]]:
        trip: Optional[Trip] = self._get.get_trip_by_id(trip_id)
        if trip is None:
            return None
        return self._serialize(trip)

    # GET /trips
    def handle_list_trips(self) -> List[Dict[str, Any]]:
        trips = self._get.get_all_trips()
        return [self._serialize(t) for t in trips]

    @staticmethod
    def _serialize(trip: Trip) -> Dict[str, Any]:
        return {
            "id": str(trip.id),
            "title": trip.title,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "budget": trip.budget,
            "description": trip.description,
            "routes": [
                {
                    "id": str(r.id),
                    "origin": r.origin,
                    "destination": r.destination,
                    "distance_km": r.distance_km,
                    "transport": r.transport,
                }
                for r in trip.routes
            ],
            "notes": [
                {
                    "id": str(n.id),
                    "content": n.content,
                    "created_at": n.created_at.isoformat(),
                }
                for n in trip.notes
            ],
        }
