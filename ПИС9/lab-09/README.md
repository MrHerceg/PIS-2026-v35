# Поехали! — Protocol Buffers и gRPC

**Дисциплина:** Проектирование интернет-систем  
**Лабораторная работа №9**  
**Тема:** Protocol Buffers и gRPC  
**Вариант:** №35 — «Поехали!»  
**Питч:** Планы, которые сбываются.  
**Ядро домена:** Маршруты, Места, Даты, Бюджет, Заметки  
**Цель:** Заменить REST API на gRPC для межсервисной коммуникации.

---

## Структура проекта

```
pis9/
├── travel_service.proto       # Протофайл: сервис, сообщения
├── grpc/
│   ├── server.py              # gRPC-сервер (TravelService)
│   ├── client.py              # gRPC-клиент (демонстрация)
│   ├── travel_pb2.py          # Сгенерировано из .proto (protobuf-классы)
│   └── travel_pb2_grpc.py     # Сгенерировано из .proto (stub/servicer)
├── generate_proto.sh          # Скрипт регенерации pb2-файлов
├── requirements.txt
└── README.md
```

---

## Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## Запуск

### 1. Запустить gRPC-сервер

```bash
cd grpc
python server.py
# gRPC server started on 50051
```

### 2. В другом терминале — запустить клиент

```bash
cd grpc
python client.py
```

**Пример вывода:**
```
CreateRoute: route_id: "1"
status: "PLANNED"

GetRoute: route_id: "1"
user_id: "user42"
title: "Paris Trip"
start_date: "2026-07-01"
end_date: "2026-07-10"
budget: 2500
status: "PLANNED"

Place updates:
route_id: "1"  place_name: "Eiffel Tower"  visit_date: "2026-07-01"  note: "Must visit at sunset"
route_id: "1"  place_name: "Louvre Museum" visit_date: "2026-07-02"  note: "Book tickets in advance"
route_id: "1"  place_name: "Notre-Dame"    visit_date: "2026-07-03"  note: "Reconstruction ongoing"
```

---

## Регенерация pb2-файлов

Если изменили `.proto`:

```bash
bash generate_proto.sh
```

или вручную:

```bash
python3 -m grpc_tools.protoc -I. --python_out=grpc --grpc_python_out=grpc travel_service.proto
```

---

## gRPC-сервис: TravelService

| Метод               | Тип                   | Описание                                  |
|---------------------|-----------------------|-------------------------------------------|
| `CreateRoute`       | Unary                 | Создаёт маршрут, возвращает route_id      |
| `GetRoute`          | Unary                 | Возвращает данные маршрута по ID          |
| `StreamPlaceUpdates`| Server-Side Streaming | Стрим обновлений мест маршрута в реальном времени |

### Сообщения

| Сообщение              | Поля                                                        |
|------------------------|-------------------------------------------------------------|
| `CreateRouteRequest`   | user_id, title, start_date, end_date, budget                |
| `CreateRouteResponse`  | route_id, status                                            |
| `GetRouteRequest`      | route_id                                                    |
| `RouteDto`             | route_id, user_id, title, start_date, end_date, budget, status |
| `StreamPlaceRequest`   | route_id                                                    |
| `PlaceUpdate`          | route_id, place_name, visit_date, note, timestamp           |

---

## Server-Side Streaming

Сценарий:
1. Клиент подписывается на `StreamPlaceUpdates` для конкретного маршрута
2. Сервер отправляет несколько сообщений с названиями мест, датами посещения и заметками
3. Вывод отображается в консоли — имитация real-time обновления плана поездки
