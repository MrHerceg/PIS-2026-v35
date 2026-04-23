import pytest
from domain.entities.note import Note
from domain.entities.route import Route
from domain.value_objects.location import Location
from domain.exceptions.domain_exceptions import InvalidRouteException, InvalidNoteException


# ─────────────────────────── Note ────────────────────────────────────────────

class TestNote:
    def test_valid_note(self):
        note = Note("Buy train tickets")
        assert note.text == "Buy train tickets"
        assert note.id is not None
        assert note.created_at is not None

    def test_empty_text_raises(self):
        with pytest.raises(InvalidNoteException):
            Note("")

    def test_whitespace_text_raises(self):
        with pytest.raises(InvalidNoteException):
            Note("   ")

    def test_text_is_stripped(self):
        note = Note("  Hello  ")
        assert note.text == "Hello"

    def test_unique_ids(self):
        n1 = Note("Note 1")
        n2 = Note("Note 2")
        assert n1.id != n2.id


# ─────────────────────────── Route ───────────────────────────────────────────

class TestRoute:
    def _locations(self, *names):
        return [Location(n) for n in names]

    def test_valid_route(self):
        route = Route(self._locations("Paris", "Lyon"))
        assert len(route.locations) == 2

    def test_single_location_raises(self):
        with pytest.raises(InvalidRouteException):
            Route(self._locations("Paris"))

    def test_empty_locations_raises(self):
        with pytest.raises(InvalidRouteException):
            Route([])

    def test_add_location(self):
        route = Route(self._locations("Paris", "Lyon"))
        route.add_location(Location("Marseille"))
        assert len(route.locations) == 3

    def test_remove_location(self):
        route = Route(self._locations("Paris", "Lyon", "Marseille"))
        route.remove_location(1)
        assert len(route.locations) == 2

    def test_remove_below_minimum_raises(self):
        route = Route(self._locations("Paris", "Lyon"))
        with pytest.raises(InvalidRouteException):
            route.remove_location(0)

    def test_reorder(self):
        route = Route(self._locations("Paris", "Lyon", "Marseille"))
        route.reorder([2, 0, 1])
        assert route.locations[0].name == "Marseille"
        assert route.locations[1].name == "Paris"

    def test_unique_ids(self):
        r1 = Route(self._locations("A", "B"))
        r2 = Route(self._locations("A", "B"))
        assert r1.id != r2.id
