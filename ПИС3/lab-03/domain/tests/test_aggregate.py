import pytest
from domain.entities.trip import Trip
from domain.value_objects.date_range import DateRange
from domain.value_objects.money import Money
from domain.value_objects.location import Location
from domain.events.trip_created import TripCreated
from domain.events.route_planned import RoutePlanned
from domain.events.trip_completed import TripCompleted
from domain.exceptions.domain_exceptions import (
    TripAlreadyCompletedException,
    InvalidRouteException,
)


def make_trip(name="Weekend in Paris", start="2026-05-01", end="2026-05-03") -> Trip:
    return Trip(name, DateRange(start, end))


# ─────────────────────────── Создание ────────────────────────────────────────

class TestTripCreation:
    def test_trip_created_event_emitted(self):
        trip = make_trip()
        events = trip.pull_events()
        assert any(isinstance(e, TripCreated) for e in events)

    def test_default_budget_is_zero(self):
        trip = make_trip()
        assert trip.budget.amount == 0

    def test_not_completed_by_default(self):
        trip = make_trip()
        assert trip.completed is False

    def test_unique_ids(self):
        t1 = make_trip()
        t2 = make_trip()
        assert t1.id != t2.id

    def test_empty_name_raises(self):
        with pytest.raises(ValueError):
            Trip("", DateRange("2026-05-01", "2026-05-03"))


# ─────────────────────────── Завершение ──────────────────────────────────────

class TestTripCompletion:
    def test_trip_completion(self):
        trip = make_trip()
        trip.complete()
        assert trip.completed is True

    def test_trip_completed_event_emitted(self):
        trip = make_trip()
        trip.pull_events()  # сбрасываем TripCreated
        trip.complete()
        events = trip.pull_events()
        assert any(isinstance(e, TripCompleted) for e in events)

    def test_cannot_complete_twice(self):
        trip = make_trip()
        trip.complete()
        with pytest.raises(TripAlreadyCompletedException):
            trip.complete()


# ─────────────────────────── Бюджет ──────────────────────────────────────────

class TestTripBudget:
    def test_change_budget(self):
        trip = make_trip()
        trip.change_budget(Money(500, "USD"))
        assert trip.budget.amount == 500
        assert trip.budget.currency == "USD"

    def test_cannot_change_completed_trip_budget(self):
        trip = make_trip()
        trip.complete()
        with pytest.raises(TripAlreadyCompletedException):
            trip.change_budget(Money(500, "USD"))


# ─────────────────────────── Маршрут ─────────────────────────────────────────

class TestTripRoute:
    def test_add_route(self):
        trip = make_trip()
        locations = [Location("Paris"), Location("Lyon")]
        trip.add_route(locations)
        assert trip.route == locations

    def test_route_planned_event_emitted(self):
        trip = make_trip()
        trip.pull_events()
        trip.add_route([Location("Paris"), Location("Lyon")])
        events = trip.pull_events()
        assert any(isinstance(e, RoutePlanned) for e in events)

    def test_route_with_single_location_raises(self):
        trip = make_trip()
        with pytest.raises(InvalidRouteException):
            trip.add_route([Location("Paris")])

    def test_cannot_add_route_to_completed_trip(self):
        trip = make_trip()
        trip.complete()
        with pytest.raises(TripAlreadyCompletedException):
            trip.add_route([Location("A"), Location("B")])


# ─────────────────────────── Заметки ─────────────────────────────────────────

class TestTripNotes:
    def test_add_note(self):
        trip = make_trip()
        note = trip.add_note("Pack umbrella")
        assert len(trip.notes) == 1
        assert note.text == "Pack umbrella"

    def test_multiple_notes(self):
        trip = make_trip()
        trip.add_note("Note 1")
        trip.add_note("Note 2")
        assert len(trip.notes) == 2

    def test_cannot_add_note_to_completed_trip(self):
        trip = make_trip()
        trip.complete()
        with pytest.raises(TripAlreadyCompletedException):
            trip.add_note("Too late")


# ─────────────────────────── События ─────────────────────────────────────────

class TestTripEvents:
    def test_pull_events_clears_queue(self):
        trip = make_trip()
        trip.pull_events()
        assert trip.pull_events() == []

    def test_invalid_date_range(self):
        with pytest.raises(ValueError):
            DateRange("2026-06-05", "2026-06-01")

    def test_empty_location(self):
        with pytest.raises(ValueError):
            Location("")
