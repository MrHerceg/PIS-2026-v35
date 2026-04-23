# ЛР №7 — CQRS: Разделение моделей чтения/записи
**«Поехали!»** · Вариант 35 · БрГТУ · Кафедра ИИТ

## Структура проекта

```
lab-07/
└── cqrs/
    ├── write_model/
    │   └── trip.py              # Агрегат Trip (инварианты, бизнес-методы)
    ├── read_model/
    │   └── trip_view.py         # Проекция TripView (денормализованная)
    └── projection/
        └── trip_projection.py   # Обработчик событий — синхронизация
                                 # Read Model через TripCreated,
                                 # PlaceAddedToRoute, NoteAdded,
                                 # TripCompleted, BudgetUpdated
tests/
    ├── test_write_model.py      # Инварианты агрегата Trip
    ├── test_read_model.py       # Поля TripView
    └── test_projection.py       # Event-Driven синхронизация + полный сценарий
```

## Запуск тестов

```bash
pip install pytest
pytest -v
```
