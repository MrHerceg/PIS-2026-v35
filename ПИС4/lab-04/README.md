# Поездки «Поехали!» — Уровень приложения (CQRS)

**Дисциплина:** Проектирование интернет-систем  
**Лабораторная работа №4**  
**Тема:** Уровень приложения  
**Вариант:** №35 — «Поездки "Поехали!"»  
**Питч:** Планы, которые сбываются.  
**Ядро домена:** Маршруты, Места, Даты, Бюджет, Заметки

---

## Структура проекта

```
pis4/
├── domain/
│   └── models/
│       └── trip.py                  # Trip, Place, Note, TripStatus
│
├── application/
│   ├── ports.py                     # Абстрактные порты (TripRepository, GeoService, NotificationService)
│   │
│   ├── command/                     # ── COMMANDS (запись) ──
│   │   ├── create_trip_command.py   # CreateTripCommand + валидация
│   │   ├── add_place_command.py     # AddPlaceToRouteCommand + валидация
│   │   ├── add_note_command.py      # AddNoteCommand + валидация
│   │   └── handlers/
│   │       ├── create_trip_handler.py   # CreateTripHandler
│   │       ├── add_place_handler.py     # AddPlaceToRouteHandler
│   │       └── add_note_handler.py      # AddNoteHandler
│   │
│   ├── query/                       # ── QUERIES (чтение) ──
│   │   ├── get_trip_by_id_query.py  # GetTripByIdQuery
│   │   ├── list_trips_query.py      # ListTripsByOwnerQuery
│   │   ├── dto/
│   │   │   └── trip_dto.py          # TripDto (Read model)
│   │   └── handlers/
│   │       ├── get_trip_by_id_handler.py  # GetTripByIdHandler
│   │       └── list_trips_handler.py      # ListTripsByOwnerHandler
│   │
│   └── service/
│       └── trip_service.py          # TripService — фасад CQRS
│
├── infrastructure/
│   └── repository/
│       ├── in_memory_trip_repository.py  # In-memory реализация TripRepository
│       ├── stub_geo_service.py           # Заглушка GeoService
│       └── stub_notification_service.py  # Заглушка NotificationService
│
└── main.py                          # Точка входа и демонстрация
```

---

## Запуск

```bash
python3 main.py
```

Требования: Python 3.8+, сторонние библиотеки не нужны.

---

## Паттерн CQRS

| Сторона   | Элемент                    | Файл |
|-----------|----------------------------|------|
| **Command** | CreateTripCommand        | `application/command/create_trip_command.py` |
| **Command** | AddPlaceToRouteCommand   | `application/command/add_place_command.py` |
| **Command** | AddNoteCommand           | `application/command/add_note_command.py` |
| **Handler** | CreateTripHandler        | `application/command/handlers/create_trip_handler.py` |
| **Handler** | AddPlaceToRouteHandler   | `application/command/handlers/add_place_handler.py` |
| **Handler** | AddNoteHandler           | `application/command/handlers/add_note_handler.py` |
| **Query**   | GetTripByIdQuery         | `application/query/get_trip_by_id_query.py` |
| **Query**   | ListTripsByOwnerQuery    | `application/query/list_trips_query.py` |
| **DTO**     | TripDto                  | `application/query/dto/trip_dto.py` |
| **Handler** | GetTripByIdHandler       | `application/query/handlers/get_trip_by_id_handler.py` |
| **Handler** | ListTripsByOwnerHandler  | `application/query/handlers/list_trips_handler.py` |
| **Фасад**   | TripService              | `application/service/trip_service.py` |
