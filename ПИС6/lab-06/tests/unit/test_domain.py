import pytest
from datetime import date
from domain.models.trip import Trip
from domain.models.route import Place
from domain.models.note import Note


def test_trip_creation_sets_planned_status():
    """Новая поездка создаётся со статусом PLANNED"""
    trip = Trip(
        trip_id="t-001", owner_id="user-1",
        title="Летний отпуск",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 7, 15),
        budget=1500.0
    )
    assert trip.status == "PLANNED"
    assert trip.route_ids == []
    assert trip.notes == []


def test_trip_validate_dates_correct():
    """Корректный диапазон дат проходит валидацию"""
    trip = Trip(
        trip_id="t-002", owner_id="user-1",
        title="Зимний тур",
        start_date=date(2026, 12, 1),
        end_date=date(2026, 12, 10),
        budget=800.0
    )
    assert trip.validate_dates() is True


def test_trip_validate_dates_invalid():
    """end_date раньше start_date — валидация возвращает False"""
    trip = Trip(
        trip_id="t-003", owner_id="user-1",
        title="Ошибочная поездка",
        start_date=date(2026, 8, 20),
        end_date=date(2026, 8, 10),
        budget=200.0
    )
    assert trip.validate_dates() is False


def test_add_place_to_route():
    """Метод add_place добавляет место в маршрут без дублей"""
    trip = Trip(
        trip_id="t-004", owner_id="user-1",
        title="Рим и Флоренция",
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 14),
        budget=2000.0
    )
    trip.add_place("place-rome")
    trip.add_place("place-florence")
    trip.add_place("place-rome")  # дубль — не должен добавиться
    assert len(trip.route_ids) == 2
    assert "place-rome" in trip.route_ids


def test_add_note_to_trip():
    """Метод add_note добавляет заметку к поездке"""
    trip = Trip(
        trip_id="t-005", owner_id="user-1",
        title="Поездка с заметками",
        start_date=date(2026, 5, 1),
        end_date=date(2026, 5, 7),
        budget=500.0
    )
    trip.add_note("Взять адаптер для розеток")
    trip.add_note("Забронировать отель заранее")
    assert len(trip.notes) == 2
    assert "Взять адаптер для розеток" in trip.notes


def test_place_is_immutable():
    """Value Object Place нельзя изменить после создания"""
    place = Place(
        place_id="p-001", name="Колизей",
        country="Италия",
        latitude=41.89, longitude=12.49,
        est_cost=25.0
    )
    with pytest.raises(Exception):
        place.name = "Форум"
