import pytest
from datetime import date
from unittest.mock import Mock, MagicMock
from application.command.create_trip_command import CreateTripCommand
from application.command.handlers.create_trip_handler import \
    CreateTripHandler
from application.command.add_place_command import AddPlaceToRouteCommand
from application.command.handlers.add_place_handler import \
    AddPlaceToRouteHandler
from application.query.get_trip_by_id_query import GetTripByIdQuery
from application.query.handlers.get_trip_by_id_handler import \
    GetTripByIdHandler


def test_create_trip_handler_saves_to_repository():
    """CreateTripHandler вызывает repository.save с корректными данными"""
    mock_repo   = Mock()
    mock_notify = Mock()
    handler = CreateTripHandler(mock_repo, mock_notify)
    command = CreateTripCommand(
        owner_id="user-1", title="Летний отпуск",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 7, 15),
        budget=1500.0
    )
    trip_id = handler.handle(command)
    assert trip_id is not None
    mock_repo.save.assert_called_once()
    mock_notify.notify_trip_created.assert_called_once_with(
        trip_id, 'user-1'
    )


def test_create_trip_handler_no_notification_when_service_absent():
    """Без notification_service обработчик не падает"""
    mock_repo = Mock()
    handler   = CreateTripHandler(mock_repo, notification_service=None)
    command = CreateTripCommand(
        owner_id="user-2", title="Тихий отдых",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 7),
        budget=300.0
    )
    trip_id = handler.handle(command)
    assert trip_id is not None


def test_add_place_handler_raises_when_trip_not_found():
    """AddPlaceToRouteHandler бросает ValueError если поездка не найдена"""
    mock_repo = Mock()
    mock_repo.find_by_id.return_value = None
    mock_geo  = Mock()
    handler = AddPlaceToRouteHandler(mock_repo, mock_geo)
    command = AddPlaceToRouteCommand(trip_id="ghost-id", place_id="p-1")
    with pytest.raises(ValueError, match='not found'):
        handler.handle(command)


def test_get_trip_by_id_handler_returns_dto():
    """GetTripByIdHandler возвращает TripDto при наличии поездки"""
    mock_trip = MagicMock()
    mock_trip.id         = "t-100"
    mock_trip.owner_id   = "user-1"
    mock_trip.title      = "Париж"
    mock_trip.start_date = date(2026, 6, 1)
    mock_trip.end_date   = date(2026, 6, 10)
    mock_trip.budget     = 1200.0
    mock_trip.status     = "PLANNED"
    mock_trip.route_ids  = []
    mock_trip.notes      = []
    mock_repo = Mock()
    mock_repo.find_by_id.return_value = mock_trip
    handler = GetTripByIdHandler(mock_repo)
    query   = GetTripByIdQuery(trip_id="t-100")
    dto     = handler.handle(query)
    assert dto is not None
    assert dto.id == "t-100"
    assert dto.title == "Париж"


def test_get_trip_by_id_handler_returns_none_when_missing():
    """GetTripByIdHandler возвращает None если поездка не найдена"""
    mock_repo = Mock()
    mock_repo.find_by_id.return_value = None
    handler = GetTripByIdHandler(mock_repo)
    query   = GetTripByIdQuery(trip_id="no-such-trip")
    result  = handler.handle(query)
    assert result is None
