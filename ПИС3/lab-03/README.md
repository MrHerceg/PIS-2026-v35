# ЛР №3 — Доменный уровень («Поехали!», Вариант 35)

## Структура проекта

```
domain/
├── entities/
│   ├── trip.py          # Aggregate Root
│   ├── route.py         # Entity
│   └── note.py          # Entity
├── value_objects/
│   ├── location.py      # Value Object
│   ├── date_range.py    # Value Object
│   └── money.py         # Value Object
├── events/
│   ├── base.py
│   ├── trip_created.py
│   ├── route_planned.py
│   └── trip_completed.py
├── exceptions/
│   └── domain_exceptions.py
└── tests/
    ├── test_value_objects.py
    ├── test_entities.py
    └── test_aggregate.py
```

## Запуск тестов

```bash
pip install pytest
pytest
```
