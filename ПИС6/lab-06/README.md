# ЛР №6 — Infrastructure Layer: Repository, REST API, БД  
**«Поехали!»** · Вариант 35 · БрГТУ · Кафедра ИИТ

## Структура проекта

```
lab-06/
├── domain/
│   └── models/
│       ├── trip.py          # Aggregate Root
│       ├── route.py         # Place (Value Object)
│       └── note.py          # Note entity
├── application/
│   ├── command/
│   │   ├── create_trip_command.py
│   │   ├── add_place_command.py
│   │   ├── update_budget_command.py
│   │   └── handlers/
│   │       ├── create_trip_handler.py
│   │       ├── add_place_handler.py
│   │       └── update_budget_handler.py
│   └── query/
│       ├── get_trip_by_id_query.py
│       ├── list_trips_by_owner_query.py
│       ├── trip_dto.py
│       └── handlers/
│           ├── get_trip_by_id_handler.py
│           └── list_trips_by_owner_handler.py
├── infrastructure/
│   ├── config/
│   │   └── database.py      # SQLAlchemy engine + session
│   └── adapter/
│       ├── in/
│       │   └── trip_controller.py   # FastAPI REST adapter
│       └── out/
│           ├── trip_orm.py                  # ORM model
│           ├── trip_repository.py           # SQLAlchemy repository
│           └── in_memory_trip_repository.py # In-memory (E2E)
└── tests/
    ├── unit/
    │   ├── test_domain.py      # Trip, Place, Note
    │   └── test_handlers.py    # Command/Query handlers (mocks)
    ├── integration/
    │   └── test_repository.py  # PostgreSQL через testcontainers
    └── e2e/
        └── test_trip_flow.py   # Полный сценарий через FastAPI TestClient
```

## Запуск

```bash
# Установить зависимости
pip install -r requirements.txt

# Только unit-тесты (без Docker)
pytest tests/unit/ -v

# E2E-тесты (без Docker)
pytest tests/e2e/ -v

# Все тесты включая интеграционные (требуется Docker для testcontainers)
pytest -v
```
