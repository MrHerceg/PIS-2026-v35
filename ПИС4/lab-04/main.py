"""
main.py — точка входа: демонстрация CQRS-архитектуры уровня приложения.

Лабораторная работа №4 — «Уровень приложения»
Вариант №35 — Поездки «Поехали!» | Питч: Планы, которые сбываются.
Ядро домена: Маршруты, Места, Даты, Бюджет, Заметки
"""
from datetime import date

from application.service.trip_service import TripService
from infrastructure.repository.in_memory_trip_repository import InMemoryTripRepository
from infrastructure.repository.stub_geo_service import StubGeoService
from infrastructure.repository.stub_notification_service import StubNotificationService


def main() -> None:
    # --- Dependency Injection (сборка зависимостей) ---
    repo = InMemoryTripRepository()
    geo = StubGeoService()
    notifier = StubNotificationService()
    service = TripService(repository=repo, geo_service=geo, notification_service=notifier)

    print("=" * 55)
    print("   CQRS-демо: Поездки «Поехали!»")
    print("=" * 55)

    # ── COMMAND: CreateTrip ──────────────────────────────────
    print("\n[CMD] CreateTripCommand → CreateTripHandler")
    trip_id = service.create_trip(
        owner_id="user_42",
        title="Минск → Брест → Варшава",
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 10),
        budget=1200.0,
    )
    print(f"      trip_id = {trip_id}")

    # ── COMMAND: AddPlaceToRoute ─────────────────────────────
    print("\n[CMD] AddPlaceToRouteCommand → AddPlaceToRouteHandler")
    for place_id in ("place_minsk", "place_brest", "place_warsaw"):
        service.add_place_to_route(trip_id=trip_id, place_id=place_id)
        print(f"      Добавлено место: {place_id}")

    # ── COMMAND: AddNote ─────────────────────────────────────
    print("\n[CMD] AddNoteCommand → AddNoteHandler")
    note_id = service.add_note(
        trip_id=trip_id,
        text="Забронировать отель в Варшаве минимум за месяц.",
    )
    print(f"      note_id = {note_id}")

    # ── QUERY: GetTripById ───────────────────────────────────
    print("\n[QRY] GetTripByIdQuery → GetTripByIdHandler")
    dto = service.get_trip_by_id(trip_id)
    if dto:
        print(f"      id:         {dto.id}")
        print(f"      title:      {dto.title}")
        print(f"      owner_id:   {dto.owner_id}")
        print(f"      dates:      {dto.start_date} → {dto.end_date}")
        print(f"      budget:     {dto.budget} BYN")
        print(f"      status:     {dto.status}")
        print(f"      route_ids:  {dto.route_ids}")
        print(f"      notes:      {dto.notes}")

    # ── Создадим ещё одну поездку того же владельца ──────────
    trip_id2 = service.create_trip(
        owner_id="user_42",
        title="Гродно → Вильнюс",
        start_date=date(2026, 8, 15),
        end_date=date(2026, 8, 20),
        budget=500.0,
    )
    service.add_place_to_route(trip_id=trip_id2, place_id="place_grodno")
    service.add_place_to_route(trip_id=trip_id2, place_id="place_vilnius")

    # ── QUERY: ListTripsByOwner ──────────────────────────────
    print("\n[QRY] ListTripsByOwnerQuery → ListTripsByOwnerHandler")
    trips = service.list_trips_by_owner(owner_id="user_42")
    print(f"      Всего поездок у user_42: {len(trips)}")
    for t in trips:
        print(f"        • [{t.id[:8]}...] {t.title} | статус: {t.status} | мест: {len(t.route_ids)}")

    # ── Фильтрация по статусу ────────────────────────────────
    print("\n[QRY] ListTripsByOwnerQuery(status='planned') → фильтрация")
    planned = service.list_trips_by_owner(owner_id="user_42", status="planned")
    print(f"      Поездок со статусом 'planned': {len(planned)}")

    print("\n" + "=" * 55)
    print("   Демонстрация завершена успешно.")
    print("=" * 55)


if __name__ == "__main__":
    main()
