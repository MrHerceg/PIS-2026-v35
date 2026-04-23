from datetime import date, datetime
from cqrs.read_model.trip_view import TripView


class TestTripView:
    def _make_view(self, **kwargs) -> TripView:
        defaults = dict(
            id="t-001",
            owner_id="user-1",
            title="Летний отпуск",
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 15),
            budget=1500.0,
            status="PLANNED",
        )
        defaults.update(kwargs)
        return TripView(**defaults)

    def test_default_place_count_is_zero(self):
        view = self._make_view()
        assert view.place_count == 0

    def test_default_note_count_is_zero(self):
        view = self._make_view()
        assert view.note_count == 0

    def test_place_count_can_be_set(self):
        view = self._make_view(place_count=3)
        assert view.place_count == 3

    def test_note_count_can_be_set(self):
        view = self._make_view(note_count=5)
        assert view.note_count == 5

    def test_status_field(self):
        view = self._make_view(status="COMPLETED")
        assert view.status == "COMPLETED"

    def test_created_at_is_datetime(self):
        view = self._make_view()
        assert isinstance(view.created_at, datetime)

    def test_view_fields_accessible(self):
        view = self._make_view()
        assert view.id == "t-001"
        assert view.owner_id == "user-1"
        assert view.title == "Летний отпуск"
        assert view.budget == 1500.0
