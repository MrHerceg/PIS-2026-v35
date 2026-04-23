# infrastructure/adapter/out/trip_repository.py
"""
PostgreSQL-реализация порта TripRepository через SQLAlchemy.
"""
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from application.ports import TripRepository
from domain.models.trip import Note, Place, Trip, TripStatus
from infrastructure.config.database import NoteORM, PlaceORM, TripORM


# ── Mapping helpers ──────────────────────────────────────────────────────────

def _orm_to_domain(orm: TripORM) -> Trip:
    trip = Trip(
        owner_id=orm.owner_id,
        title=orm.title,
        start_date=orm.start_date,
        end_date=orm.end_date,
        budget=orm.budget,
        description=orm.description,
        status=TripStatus(orm.status),
    )
    # Restore UUID from stored string
    object.__setattr__(trip, "id", __import__("uuid").UUID(orm.id))

    trip.route = [
        Place(
            place_id=p.id,
            name=p.name,
            latitude=p.latitude,
            longitude=p.longitude,
        )
        for p in orm.places
    ]
    trip.notes = [
        Note(id=__import__("uuid").UUID(n.id), text=n.text)
        for n in orm.notes
    ]
    return trip


def _domain_to_orm(trip: Trip, existing: Optional[TripORM] = None) -> TripORM:
    orm = existing or TripORM()
    orm.id          = str(trip.id)
    orm.owner_id    = trip.owner_id
    orm.title       = trip.title
    orm.description = trip.description
    orm.start_date  = trip.start_date
    orm.end_date    = trip.end_date
    orm.budget      = trip.budget
    orm.status      = trip.status.value

    orm.places = [
        PlaceORM(id=p.place_id, trip_id=str(trip.id),
                 name=p.name, latitude=p.latitude, longitude=p.longitude)
        for p in trip.route
    ]
    orm.notes = [
        NoteORM(id=str(n.id), trip_id=str(trip.id), text=n.text)
        for n in trip.notes
    ]
    return orm


# ── Repository implementation ────────────────────────────────────────────────

class SqlAlchemyTripRepository(TripRepository):
    """
    Адаптер исходящего порта TripRepository.
    Хранит поездки в PostgreSQL через SQLAlchemy ORM.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, trip: Trip) -> None:
        """Сохранение агрегата поездки (insert или update)."""
        existing = self._session.get(TripORM, str(trip.id))
        orm = _domain_to_orm(trip, existing)
        if existing is None:
            self._session.add(orm)
        self._session.commit()
        self._session.refresh(orm)

    def find_by_id(self, trip_id: str) -> Optional[Trip]:
        """Поиск поездки по ID."""
        orm = self._session.get(TripORM, trip_id)
        if orm is None:
            return None
        return _orm_to_domain(orm)

    def find_by_owner(self, owner_id: str) -> List[Trip]:
        """Список поездок пользователя."""
        rows = (
            self._session.query(TripORM)
            .filter(TripORM.owner_id == owner_id)
            .all()
        )
        return [_orm_to_domain(r) for r in rows]

    def find_active_trips(self) -> List[Trip]:
        """Список поездок со статусом, отличным от COMPLETED."""
        rows = (
            self._session.query(TripORM)
            .filter(TripORM.status != TripStatus.COMPLETED.value)
            .all()
        )
        return [_orm_to_domain(r) for r in rows]
