import pytest
from fastapi.testclient import TestClient
from infrastructure.adapter.in.trip_controller import app

client = TestClient(app)


def test_full_trip_flow():
    """Полный сценарий: Создать → Добавить место → Обновить бюджет → Получить"""
    # Шаг 1: Создать поездку
    response = client.post("/api/trips", json={
        "owner_id":   "e2e-user",
        "title":      "E2E-путешествие",
        "start_date": "2026-09-01",
        "end_date":   "2026-09-14",
        "budget":     2000.0
    })
    assert response.status_code == 200
    trip = response.json()
    trip_id = trip["id"]
    assert trip["status"] == "PLANNED"

    # Шаг 2: Добавить место в маршрут
    response = client.post(
        f"/api/trips/{trip_id}/add-place",
        params={"place_id": "place-barcelona"}
    )
    assert response.status_code == 200
    assert response.json()["place_id"] == "place-barcelona"

    # Шаг 3: Обновить бюджет
    response = client.patch(
        f"/api/trips/{trip_id}/budget",
        params={"budget": 2500.0}
    )
    assert response.status_code == 200
    assert response.json()["budget"] == 2500.0

    # Шаг 4: Получить итоговые данные
    response = client.get(f"/api/trips/{trip_id}")
    assert response.status_code == 200
    assert response.json()["id"] == trip_id


def test_create_trip_with_invalid_dates_returns_400():
    """Конфликт дат на уровне E2E возвращает 400"""
    response = client.post("/api/trips", json={
        "owner_id":   "e2e-user",
        "title":      "Ошибочная",
        "start_date": "2026-09-14",
        "end_date":   "2026-09-01",
        "budget":     500.0
    })
    assert response.status_code == 400


def test_get_nonexistent_trip_returns_404():
    """Запрос несуществующей поездки возвращает 404"""
    response = client.get("/api/trips/does-not-exist")
    assert response.status_code == 404


def test_list_trips_by_owner():
    """Список поездок возвращает только поездки указанного пользователя"""
    response = client.get("/api/trips", params={"owner_id": "e2e-user"})
    assert response.status_code == 200
    trips = response.json()
    assert isinstance(trips, list)
    assert all(t['owner_id'] == 'e2e-user' for t in trips)
