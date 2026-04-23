# application/query/get_trip_by_id_query.py
from dataclasses import dataclass


@dataclass(frozen=True)
class GetTripByIdQuery:
    """
    Запрос для получения поездки по идентификатору.

    Поля:
        trip_id — уникальный идентификатор поездки
    """
    trip_id: str
