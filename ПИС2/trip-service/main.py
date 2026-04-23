"""
main.py — точка входа: демонстрирует сборку гексагональной архитектуры.

Поездки «Поехали!» — Планы, которые сбываются.
Ядро домена: Маршруты, Места, Даты, Бюджет, Заметки
"""
import json

from application.service.trip_service import TripService
from infrastructure.adapter.in_.trip_controller import TripController
from infrastructure.adapter.out.in_memory_trip_repository import InMemoryTripRepository
from infrastructure.adapter.out.stub_geo_service import StubGeoService
from infrastructure.adapter.out.email_notification_service import EmailNotificationService
from domain.models.route import Route
from domain.models.note import Note


def main() -> None:
    # --- Wiring (Dependency Injection) ---
    repository = InMemoryTripRepository()
    geo_service = StubGeoService()
    notifier = EmailNotificationService()

    trip_service = TripService(
        trip_repository=repository,
        geo_service=geo_service,
        notification_service=notifier,
    )

    controller = TripController(
        create_trip_use_case=trip_service,
        get_trip_use_case=trip_service,
    )

    # --- POST /trips ---
    print("=== Создание поездки ===")
    response = controller.handle_create_trip({
        "title": "Минск → Брест → Варшава",
        "start_date": "2026-06-01",
        "end_date": "2026-06-10",
        "budget": 1500.00,
        "description": "Летняя поездка через Беларусь в Польшу",
    })
    print(f"Ответ: {response}\n")
    trip_id = response["id"]

    # --- Добавим маршрут и заметку напрямую в доменный объект ---
    trip = repository.find_by_id(trip_id)

    dist_mb = geo_service.calculate_distance_km("Минск", "Брест")
    route1 = Route(origin="Минск", destination="Брест", distance_km=round(dist_mb, 1), transport="train")
    trip.add_route(route1)

    dist_bw = geo_service.calculate_distance_km("Брест", "Варшава")
    route2 = Route(origin="Брест", destination="Варшава", distance_km=round(dist_bw, 1), transport="bus")
    trip.add_route(route2)

    note = Note(content="Забронировать отель в центре Варшавы за месяц до выезда.")
    trip.add_note(note)

    # --- GET /trips/<id> ---
    print("=== Получение поездки по ID ===")
    trip_data = controller.handle_get_trip(trip_id)
    print(json.dumps(trip_data, ensure_ascii=False, indent=2))

    # --- Демонстрация GeoService ---
    print("\n=== GeoService: расчёт расстояний ===")
    pairs = [("Минск", "Брест"), ("Брест", "Варшава"), ("Минск", "Вильнюс")]
    for origin, dest in pairs:
        km = geo_service.calculate_distance_km(origin, dest)
        print(f"  {origin} → {dest}: {km:.1f} км")

    # --- Уведомление ---
    print("\n=== NotificationService ===")
    notifier.notify_trip_created(trip, recipient_email="user@example.com")

    # --- GET /trips (список) ---
    print("=== Список всех поездок ===")
    all_trips = controller.handle_list_trips()
    print(f"Всего поездок: {len(all_trips)}")
    for t in all_trips:
        print(f"  [{t['id'][:8]}...] {t['title']}  |  маршрутов: {len(t['routes'])}  |  заметок: {len(t['notes'])}")


if __name__ == "__main__":
    main()
