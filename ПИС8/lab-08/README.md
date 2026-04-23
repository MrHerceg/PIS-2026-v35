# Поехали! — Микросервисы и Event Bus

**Дисциплина:** Проектирование интернет-систем  
**Лабораторная работа №8**  
**Тема:** Микросервисы и Event Bus  
**Вариант:** №35 — «Поехали!»  
**Питч:** Планы, которые сбываются.  
**Ядро домена:** Маршруты, Места, Даты, Бюджет, Заметки

---

## Архитектура

```
                        ┌─────────────────────────────────────┐
                        │          Nginx API Gateway          │
                        │            (порт 80)                │
                        └────────────┬────────────────────────┘
                                     │
               ┌─────────────────────┴──────────────────────┐
               │  /routes/**                   /places/**    │
               ▼                                             ▼
  ┌─────────────────────────┐            ┌─────────────────────────────┐
  │      Route Service      │            │   Place & Budget Service     │
  │       (порт 8001)       │            │         (порт 8002)          │
  │  Bounded Context:       │            │  Bounded Context:            │
  │  Управление маршрутами  │            │  Управление местами          │
  └────────────┬────────────┘            └──────────────┬──────────────┘
               │                                        │
               │         ┌─────────────┐               │
               └────────►│  RabbitMQ   │◄──────────────┘
                         │  Event Bus  │
                         │ (порт 5672) │
                         │ UI: 15672   │
                         └─────────────┘
               │                                        │
               ▼                                        ▼
        ┌─────────────┐                         ┌─────────────┐
        │  route-db   │                         │  place-db   │
        │  PostgreSQL │                         │  PostgreSQL │
        │ (порт 5433) │                         │ (порт 5434) │
        └─────────────┘                         └─────────────┘
```

---

## Структура проекта

```
pis8/
├── route-service/              # Сервис маршрутов
│   ├── app/
│   │   ├── main.py             # FastAPI приложение
│   │   ├── models.py           # Доменные модели
│   │   ├── database.py         # SQLAlchemy + ORM
│   │   └── events.py           # RabbitMQ publisher
│   ├── Dockerfile
│   └── requirements.txt
│
├── place-service/              # Сервис мест и бюджета
│   ├── app/
│   │   ├── main.py             # FastAPI приложение
│   │   ├── models.py           # Доменные модели
│   │   ├── database.py         # SQLAlchemy + ORM
│   │   └── events.py           # RabbitMQ publisher
│   ├── Dockerfile
│   └── requirements.txt
│
├── nginx/
│   └── nginx.conf              # API Gateway конфигурация
│
├── docker-compose.yml          # Оркестрация всех сервисов
└── README.md
```

---

## Запуск

```bash
docker compose up --build
```

---

## REST API

### Route Service (через Gateway: `http://localhost/routes/`)

| Метод | Путь               | Описание              | Событие        |
|-------|--------------------|-----------------------|----------------|
| POST  | `/routes`          | Создать маршрут       | RouteCreated   |
| GET   | `/routes/{id}`     | Получить маршрут      | —              |
| GET   | `/routes?owner_id` | Список маршрутов      | —              |

### Place & Budget Service (через Gateway: `http://localhost/places/`)

| Метод | Путь                        | Описание              | Событие        |
|-------|-----------------------------|-----------------------|----------------|
| POST  | `/routes/{id}/places`       | Добавить место        | PlaceAdded     |
| GET   | `/routes/{id}/places`       | Список мест           | —              |
| POST  | `/routes/{id}/budget`       | Задать бюджет         | BudgetUpdated  |
| GET   | `/routes/{id}/budget`       | Получить бюджет       | —              |
| POST  | `/routes/{id}/notes`        | Добавить заметку      | NoteAdded      |
| GET   | `/routes/{id}/notes`        | Список заметок        | —              |

---

## Event Bus — RabbitMQ

| Событие        | Источник        | Описание                        |
|----------------|-----------------|---------------------------------|
| RouteCreated   | route-service   | Создан новый маршрут            |
| PlaceAdded     | place-service   | Добавлено место в маршрут       |
| BudgetUpdated  | place-service   | Обновлён бюджет маршрута        |
| NoteAdded      | place-service   | Добавлена заметка к маршруту    |

Exchange: `poekhali.events` (type: topic, durable: true)

**RabbitMQ Management UI:** http://localhost:15672  
Login: `guest` / `guest`

---

## Swagger UI

- Route Service:   http://localhost:8001/docs  
- Place Service:   http://localhost:8002/docs
