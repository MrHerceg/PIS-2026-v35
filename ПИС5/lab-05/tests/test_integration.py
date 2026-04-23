# tests/test_integration.py
"""
Интеграционные тесты для системы поездок «Поехали!».

Тестируемые сценарии:
    1. Сохранение Trip → чтение из БД
    2. HTTP POST /api/trips → проверка создания записи
    3. HTTP GET /api/trips/{id} → проверка корректности ответа
    4. Валидация дат: end_date ≤ start_date → 400 Bad Request
    5. Event публикация (уведомление о создании поездки) → проверка подписчика

Запуск:
    pytest tests/test_integration.py -v
"""
import os
import pytest
from datetime import date
from unittest.mock import MagicMock

# Point SQLAlchemy at SQLite BEFORE any app imports resolve DATABASE_URL
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event as sa_event
from sqlalchemy.orm import sessionmaker

from application.ports import EventPublisher
from application.service.trip_service import TripService
from domain.models.trip import Trip, TripStatus
from infrastructure.adapter.out.notification_service import EventNotificationService
from infrastructure.adapter.out.trip_repository import SqlAlchemyTripRepository
from infrastructure.config.database import Base, get_db
from main import app

# ── Shared in-memory engine (same connection so tables persist) ───────────────
from sqlalchemy.pool import StaticPool

TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture()
def db_session():
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client():
    """TestClient that overrides get_db to use the test SQLite engine."""
    def override_get_db():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── 1. Repository: save → find_by_id ─────────────────────────────────────────

def test_save_and_find_trip(db_session):
    """Сохранение Trip → чтение из БД."""
    repo = SqlAlchemyTripRepository(db_session)
    trip = Trip(
        owner_id="user_1",
        title="Тест-поездка",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 7, 10),
        budget=800.0,
    )
    repo.save(trip)

    found = repo.find_by_id(str(trip.id))
    assert found is not None
    assert found.title == "Тест-поездка"
    assert found.owner_id == "user_1"
    assert found.budget == 800.0
    assert found.status == TripStatus.DRAFT


def test_find_active_trips(db_session):
    """find_active_trips не возвращает COMPLETED поездки."""
    repo = SqlAlchemyTripRepository(db_session)

    active = Trip(
        owner_id="u1", title="Активная",
        start_date=date(2026, 8, 1), end_date=date(2026, 8, 5), budget=300.0,
    )
    completed = Trip(
        owner_id="u1", title="Завершённая",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 5), budget=100.0,
        status=TripStatus.COMPLETED,
    )
    repo.save(active)
    repo.save(completed)

    results = repo.find_active_trips()
    titles = [t.title for t in results]
    assert "Активная" in titles
    assert "Завершённая" not in titles


# ── 2. HTTP POST /api/trips ───────────────────────────────────────────────────

def test_post_create_trip(client):
    """HTTP POST /api/trips → 201 + id в ответе."""
    payload = {
        "owner_id": "user_42",
        "title": "Минск → Варшава",
        "start_date": "2026-06-01",
        "end_date": "2026-06-10",
        "budget": 1200.0,
    }
    response = client.post("/api/trips", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "created"


# ── 3. HTTP GET /api/trips/{id} ───────────────────────────────────────────────

def test_get_trip_by_id(client):
    """POST → GET /api/trips/{id} → корректные данные."""
    payload = {
        "owner_id": "user_5",
        "title": "Брест → Гродно",
        "start_date": "2026-09-01",
        "end_date": "2026-09-05",
        "budget": 500.0,
    }
    create_resp = client.post("/api/trips", json=payload)
    assert create_resp.status_code == 201
    trip_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/trips/{trip_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == trip_id
    assert data["title"] == "Брест → Гродно"
    assert data["owner_id"] == "user_5"
    assert data["status"] == "draft"


def test_get_trip_not_found(client):
    """GET /api/trips/{id} с несуществующим id → 404."""
    response = client.get("/api/trips/nonexistent-id-000")
    assert response.status_code == 404


# ── 4. Валидация дат ──────────────────────────────────────────────────────────

def test_create_trip_invalid_dates(client):
    """end_date < start_date → 422 Validation Error."""
    payload = {
        "owner_id": "user_1",
        "title": "Плохие даты",
        "start_date": "2026-06-10",
        "end_date": "2026-06-01",
        "budget": 100.0,
    }
    response = client.post("/api/trips", json=payload)
    assert response.status_code == 422


def test_create_trip_equal_dates(client):
    """start_date == end_date → 422."""
    payload = {
        "owner_id": "user_1",
        "title": "Одинаковые даты",
        "start_date": "2026-06-01",
        "end_date": "2026-06-01",
        "budget": 100.0,
    }
    response = client.post("/api/trips", json=payload)
    assert response.status_code == 422


def test_create_trip_negative_budget(client):
    """budget < 0 → 422."""
    payload = {
        "owner_id": "user_1",
        "title": "Отрицательный бюджет",
        "start_date": "2026-06-01",
        "end_date": "2026-06-10",
        "budget": -100.0,
    }
    response = client.post("/api/trips", json=payload)
    assert response.status_code == 422


# ── 5. Event публикация ───────────────────────────────────────────────────────

def test_event_published_on_trip_created(db_session):
    """Создание поездки → EventPublisher.publish вызван с event_type='trip.created'."""
    mock_publisher = MagicMock(spec=EventPublisher)
    notifier = EventNotificationService(publisher=mock_publisher)

    repo = SqlAlchemyTripRepository(db_session)
    service = TripService(
        repository=repo,
        geo_service=None,
        notification_service=notifier,
    )

    trip_id = service.create_trip(
        owner_id="user_99",
        title="Событийная поездка",
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 7),
        budget=600.0,
    )

    mock_publisher.publish.assert_called_once()
    # Check that event_type='trip.created' was passed as keyword arg
    call_kwargs = mock_publisher.publish.call_args.kwargs
    assert call_kwargs.get("event_type") == "trip.created"
    assert trip_id in str(call_kwargs)
