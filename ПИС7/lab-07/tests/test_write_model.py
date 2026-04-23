import pytest
from datetime import date
from cqrs.write_model.trip import Trip


def make_trip(**kwargs) -> Trip:
    defaults = dict(
        trip_id="t-001",
        owner_id="user-1",
        title="Летний отпуск",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 7, 15),
        budget=1500.0,
    )
    defaults.update(kwargs)
    return Trip(**defaults)


# ─── Создание ───────────────────────────────────────────────────────────────

class TestTripCreation:
    def test_valid_trip_has_planned_status(self):
        trip = make_trip()
        assert trip.status == "PLANNED"

    def test_valid_trip_has_empty_route(self):
        trip = make_trip()
        assert trip.route_ids == []

    def test_valid_trip_has_empty_notes(self):
        trip = make_trip()
        assert trip.notes == []

    def test_end_date_equal_to_start_date_raises(self):
        """end_date == start_date должен выбрасывать ValueError"""
        with pytest.raises(ValueError, match="end_date must be after start_date"):
            make_trip(start_date=date(2026, 7, 1), end_date=date(2026, 7, 1))

    def test_end_date_before_start_date_raises(self):
        """end_date < start_date должен выбрасывать ValueError"""
        with pytest.raises(ValueError, match="end_date must be after start_date"):
            make_trip(start_date=date(2026, 8, 10), end_date=date(2026, 8, 1))

    def test_negative_budget_raises(self):
        """Отрицательный бюджет должен выбрасывать ValueError"""
        with pytest.raises(ValueError, match="budget must be non-negative"):
            make_trip(budget=-100.0)

    def test_zero_budget_is_valid(self):
        trip = make_trip(budget=0.0)
        assert trip.budget == 0.0


# ─── add_place ───────────────────────────────────────────────────────────────

class TestAddPlace:
    def test_add_place_appends_to_route(self):
        trip = make_trip()
        trip.add_place("place-paris")
        assert "place-paris" in trip.route_ids

    def test_add_multiple_places(self):
        trip = make_trip()
        trip.add_place("place-paris")
        trip.add_place("place-lyon")
        assert len(trip.route_ids) == 2

    def test_add_duplicate_place_raises(self):
        """Одно и то же место нельзя добавить дважды"""
        trip = make_trip()
        trip.add_place("place-paris")
        with pytest.raises(ValueError, match="already in route"):
            trip.add_place("place-paris")

    def test_add_place_to_completed_trip_raises(self):
        """Нельзя добавить место в завершённую поездку"""
        trip = make_trip()
        trip.complete()
        with pytest.raises(ValueError, match="Cannot modify a completed trip"):
            trip.add_place("place-rome")


# ─── add_note ────────────────────────────────────────────────────────────────

class TestAddNote:
    def test_add_note_appends_text(self):
        trip = make_trip()
        trip.add_note("Взять адаптер для розеток")
        assert "Взять адаптер для розеток" in trip.notes

    def test_add_note_strips_whitespace(self):
        trip = make_trip()
        trip.add_note("  Забронировать отель  ")
        assert "Забронировать отель" in trip.notes

    def test_add_empty_note_raises(self):
        trip = make_trip()
        with pytest.raises(ValueError, match="Note text cannot be empty"):
            trip.add_note("")

    def test_add_whitespace_only_note_raises(self):
        trip = make_trip()
        with pytest.raises(ValueError, match="Note text cannot be empty"):
            trip.add_note("   ")


# ─── complete ────────────────────────────────────────────────────────────────

class TestComplete:
    def test_complete_sets_status(self):
        trip = make_trip()
        trip.complete()
        assert trip.status == "COMPLETED"

    def test_complete_twice_raises(self):
        trip = make_trip()
        trip.complete()
        with pytest.raises(ValueError, match="Trip is already completed"):
            trip.complete()
