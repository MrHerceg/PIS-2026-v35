import pytest
from datetime import date
from cqrs.projection.trip_projection import TripProjection


def make_created_event(trip_id="t-001", owner_id="user-1",
                       title="Поездка", budget=1000.0) -> dict:
    return {
        "event":      "TripCreated",
        "trip_id":    trip_id,
        "owner_id":   owner_id,
        "title":      title,
        "start_date": date(2026, 8, 1),
        "end_date":   date(2026, 8, 14),
        "budget":     budget,
    }


# ─── TripCreated ─────────────────────────────────────────────────────────────

class TestTripCreated:
    def test_creates_trip_view(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        view = proj.get("t-001")
        assert view is not None
        assert view.id == "t-001"

    def test_initial_status_is_planned(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        assert proj.get("t-001").status == "PLANNED"

    def test_initial_place_count_zero(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        assert proj.get("t-001").place_count == 0

    def test_initial_note_count_zero(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        assert proj.get("t-001").note_count == 0

    def test_stores_owner_and_title(self):
        proj = TripProjection()
        proj.handle(make_created_event(owner_id="user-99", title="Барселона"))
        view = proj.get("t-001")
        assert view.owner_id == "user-99"
        assert view.title == "Барселона"


# ─── PlaceAddedToRoute ────────────────────────────────────────────────────────

class TestPlaceAddedToRoute:
    def test_increments_place_count(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-001"})
        assert proj.get("t-001").place_count == 1

    def test_increments_place_count_multiple_times(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-001"})
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-001"})
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-001"})
        assert proj.get("t-001").place_count == 3

    def test_unknown_trip_id_does_not_raise(self):
        proj = TripProjection()
        # Не должно выбрасывать исключение
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "ghost-id"})


# ─── NoteAdded ───────────────────────────────────────────────────────────────

class TestNoteAdded:
    def test_increments_note_count(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        proj.handle({"event": "NoteAdded", "trip_id": "t-001"})
        assert proj.get("t-001").note_count == 1

    def test_increments_note_count_multiple_times(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        proj.handle({"event": "NoteAdded", "trip_id": "t-001"})
        proj.handle({"event": "NoteAdded", "trip_id": "t-001"})
        assert proj.get("t-001").note_count == 2

    def test_note_count_independent_of_place_count(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-001"})
        proj.handle({"event": "NoteAdded", "trip_id": "t-001"})
        proj.handle({"event": "NoteAdded", "trip_id": "t-001"})
        assert proj.get("t-001").place_count == 1
        assert proj.get("t-001").note_count == 2


# ─── TripCompleted ───────────────────────────────────────────────────────────

class TestTripCompleted:
    def test_sets_status_to_completed(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        proj.handle({"event": "TripCompleted", "trip_id": "t-001"})
        assert proj.get("t-001").status == "COMPLETED"

    def test_completed_does_not_reset_counts(self):
        proj = TripProjection()
        proj.handle(make_created_event())
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-001"})
        proj.handle({"event": "NoteAdded",         "trip_id": "t-001"})
        proj.handle({"event": "TripCompleted",     "trip_id": "t-001"})
        view = proj.get("t-001")
        assert view.place_count == 1
        assert view.note_count  == 1


# ─── BudgetUpdated ───────────────────────────────────────────────────────────

class TestBudgetUpdated:
    def test_updates_budget(self):
        proj = TripProjection()
        proj.handle(make_created_event(budget=1000.0))
        proj.handle({"event": "BudgetUpdated", "trip_id": "t-001", "new_budget": 2500.0})
        assert proj.get("t-001").budget == 2500.0

    def test_budget_can_be_updated_multiple_times(self):
        proj = TripProjection()
        proj.handle(make_created_event(budget=1000.0))
        proj.handle({"event": "BudgetUpdated", "trip_id": "t-001", "new_budget": 1500.0})
        proj.handle({"event": "BudgetUpdated", "trip_id": "t-001", "new_budget": 3000.0})
        assert proj.get("t-001").budget == 3000.0


# ─── get_by_owner ─────────────────────────────────────────────────────────────

class TestGetByOwner:
    def test_returns_all_trips_for_owner(self):
        proj = TripProjection()
        proj.handle(make_created_event(trip_id="t-A", owner_id="owner-X"))
        proj.handle(make_created_event(trip_id="t-B", owner_id="owner-X"))
        proj.handle(make_created_event(trip_id="t-C", owner_id="owner-Y"))
        results = proj.get_by_owner("owner-X")
        assert len(results) == 2
        assert all(v.owner_id == "owner-X" for v in results)

    def test_returns_empty_list_for_unknown_owner(self):
        proj = TripProjection()
        proj.handle(make_created_event(trip_id="t-A", owner_id="owner-X"))
        results = proj.get_by_owner("nobody")
        assert results == []


# ─── Полный сценарий (интеграционный) ───────────────────────────────────────

class TestFullScenario:
    def test_full_event_flow(self):
        """TripCreated → 2×PlaceAdded → 1×NoteAdded → BudgetUpdated → TripCompleted"""
        proj = TripProjection()

        proj.handle(make_created_event(trip_id="t-full", owner_id="user-1",
                                       title="Испания", budget=2000.0))
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-full"})
        proj.handle({"event": "PlaceAddedToRoute", "trip_id": "t-full"})
        proj.handle({"event": "NoteAdded",         "trip_id": "t-full"})
        proj.handle({"event": "BudgetUpdated",     "trip_id": "t-full",
                     "new_budget": 2800.0})
        proj.handle({"event": "TripCompleted",     "trip_id": "t-full"})

        view = proj.get("t-full")
        assert view.place_count == 2
        assert view.note_count  == 1
        assert view.budget      == 2800.0
        assert view.status      == "COMPLETED"
