import pytest
from datetime import date
from testcontainers.postgres import PostgresContainer
from infrastructure.config.database import Base, engine, SessionLocal
from infrastructure.adapter.out.trip_repository import \
    SQLAlchemyTripRepository


@pytest.fixture(scope='module')
def postgres():
    with PostgresContainer("postgres:15") as pg:
        yield pg


@pytest.fixture(scope='module')
def repo(postgres):
    Base.metadata.create_all(engine)
    return SQLAlchemyTripRepository()


def test_save_and_find_by_id(repo):
    """Сохранённая поездка корректно читается по ID"""
    trip = {
        "id":         "t-int-001",
        "owner_id":   "user-integration",
        "title":      "Интеграционный тест",
        "start_date": date(2026, 10, 1),
        "end_date":   date(2026, 10, 10),
        "budget":     900.0,
        "status":     "PLANNED"
    }
    repo.save(trip)
    fetched = repo.find_by_id("t-int-001")
    assert fetched is not None
    assert fetched.id == "t-int-001"
    assert fetched.title == "Интеграционный тест"
    assert fetched.status == "PLANNED"


def test_find_by_owner_returns_list(repo):
    """find_by_owner возвращает все поездки пользователя"""
    for i in range(3):
        repo.save({
            "id":         f"t-owner-{i}",
            "owner_id":   "owner-batch",
            "title":      f"Поездка {i}",
            "start_date": date(2026, i + 1, 1),
            "end_date":   date(2026, i + 1, 10),
            "budget":     500.0,
            "status":     "PLANNED"
        })
    results = repo.find_by_owner("owner-batch")
    assert len(results) == 3


def test_find_active_trips_excludes_completed(repo):
    """find_active_trips не возвращает завершённые поездки"""
    repo.save({
        "id":         "t-done",
        "owner_id":   "user-done",
        "title":      "Завершённая поездка",
        "start_date": date(2026, 1, 1),
        "end_date":   date(2026, 1, 5),
        "budget":     100.0,
        "status":     "COMPLETED"
    })
    active = repo.find_active_trips()
    ids = [t.id for t in active]
    assert "t-done" not in ids
