# Поездки «Поехали!» — Infrastructure Layer

**Дисциплина:** Проектирование интернет-систем  
**Лабораторная работа №5**  
**Тема:** Infrastructure Layer: Repository, REST API, БД  
**Вариант:** №35 — «Поездки "Поехали!"»  
**Питч:** Планы, которые сбываются.

---

## Структура проекта

```
pis5/
├── domain/
│   └── models/
│       └── trip.py                              # Trip, Place, Note, TripStatus
│
├── application/
│   ├── ports.py                                 # Абстрактные порты
│   ├── command/
│   │   ├── create_trip_command.py
│   │   ├── add_place_command.py
│   │   ├── add_note_command.py
│   │   └── handlers/
│   │       ├── create_trip_handler.py
│   │       ├── add_place_handler.py
│   │       └── add_note_handler.py
│   ├── query/
│   │   ├── get_trip_by_id_query.py
│   │   ├── list_trips_query.py
│   │   ├── dto/trip_dto.py
│   │   └── handlers/
│   │       ├── get_trip_by_id_handler.py
│   │       └── list_trips_handler.py
│   └── service/
│       └── trip_service.py                      # Фасад CQRS
│
├── infrastructure/
│   ├── config/
│   │   └── database.py                          # SQLAlchemy engine, ORM-модели, get_db
│   └── adapter/
│       ├── in/
│       │   └── trip_controller.py               # FastAPI REST Controller
│       └── out/
│           ├── trip_repository.py               # SQLAlchemy PostgreSQL Repository
│           ├── rabbitmq_event_publisher.py      # RabbitMQ EventPublisher
│           └── notification_service.py          # EventNotificationService
│
├── tests/
│   └── test_integration.py                      # Интеграционные тесты (SQLite)
│
├── main.py                                      # FastAPI app entry point
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Запуск через Docker Compose

```bash
docker compose up --build
```

Swagger UI: http://localhost:8000/docs  
RabbitMQ Management: http://localhost:15672 (guest / guest)

---

## REST API

| Метод  | Путь                          | Описание                        |
|--------|-------------------------------|---------------------------------|
| POST   | `/api/trips`                  | Создать поездку                 |
| GET    | `/api/trips/{trip_id}`        | Получить поездку по ID          |
| GET    | `/api/trips?owner_id=...`     | Список поездок владельца        |
| GET    | `/api/trips/active`           | Список активных поездок         |
| POST   | `/api/trips/{trip_id}/places` | Добавить место в маршрут        |
| POST   | `/api/trips/{trip_id}/notes`  | Добавить заметку                |
| GET    | `/health`                     | Health check                    |

---

## Интеграционные тесты

```bash
pip install -r requirements.txt
pytest tests/test_integration.py -v
```

Тесты используют SQLite in-memory (не требуют запущенного PostgreSQL).

### Тестируемые сценарии

1. Сохранение Trip → чтение из БД  
2. HTTP POST `/api/trips` → проверка создания записи  
3. HTTP GET `/api/trips/{id}` → проверка корректности ответа  
4. Валидация дат: `end_date ≤ start_date` → 422  
5. Event публикация → проверка вызова `EventPublisher.publish`

---

## Технологии

| Компонент        | Технология                  |
|------------------|-----------------------------|
| REST Framework   | FastAPI + Uvicorn           |
| ORM / БД         | SQLAlchemy + PostgreSQL 15  |
| Event Bus        | RabbitMQ 3.12 (pika)        |
| Контейнеризация  | Docker + Docker Compose     |
| Тесты            | pytest + httpx + SQLite     |
