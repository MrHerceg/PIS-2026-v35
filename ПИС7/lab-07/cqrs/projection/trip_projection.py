from cqrs.read_model.trip_view import TripView
from datetime import datetime


class TripProjection:
    """Обработчик событий: синхронизирует Read Model с Write Model"""

    def __init__(self):
        self.read_db: dict = {}   # in-memory Read Store

    def handle(self, event: dict) -> None:
        """Маршрутизатор событий"""
        event_type = event.get("event")
        if event_type == "TripCreated":
            self._on_trip_created(event)
        elif event_type == "PlaceAddedToRoute":
            self._on_place_added(event)
        elif event_type == "NoteAdded":
            self._on_note_added(event)
        elif event_type == "TripCompleted":
            self._on_trip_completed(event)
        elif event_type == "BudgetUpdated":
            self._on_budget_updated(event)

    # ── обработчики ────────────────────────────────────────────

    def _on_trip_created(self, event: dict) -> None:
        trip_id = event["trip_id"]
        self.read_db[trip_id] = TripView(
            id          = trip_id,
            owner_id    = event["owner_id"],
            title       = event["title"],
            start_date  = event["start_date"],
            end_date    = event["end_date"],
            budget      = event["budget"],
            status      = "PLANNED",
            place_count = 0,
            note_count  = 0,
            created_at  = datetime.now()
        )

    def _on_place_added(self, event: dict) -> None:
        view = self.read_db.get(event["trip_id"])
        if view:
            view.place_count += 1

    def _on_note_added(self, event: dict) -> None:
        view = self.read_db.get(event["trip_id"])
        if view:
            view.note_count += 1

    def _on_trip_completed(self, event: dict) -> None:
        view = self.read_db.get(event["trip_id"])
        if view:
            view.status = "COMPLETED"

    def _on_budget_updated(self, event: dict) -> None:
        view = self.read_db.get(event["trip_id"])
        if view:
            view.budget = event["new_budget"]

    # ── чтение ─────────────────────────────────────────────────

    def get(self, trip_id: str):
        """Получить проекцию поездки по ID"""
        return self.read_db.get(trip_id)

    def get_by_owner(self, owner_id: str):
        """Получить все проекции поездок пользователя"""
        return [v for v in self.read_db.values()
                if v.owner_id == owner_id]
