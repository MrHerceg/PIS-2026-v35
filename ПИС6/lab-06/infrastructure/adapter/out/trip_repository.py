from typing import List, Optional, Union
from domain.models.trip import Trip
from infrastructure.adapter.out.trip_orm import TripORM
from infrastructure.config.database import SessionLocal


class SQLAlchemyTripRepository:
    """Адаптер порта TripRepository — работает с PostgreSQL через SQLAlchemy."""

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _to_domain(orm: TripORM) -> Trip:
        t = Trip(
            trip_id=orm.id,
            owner_id=orm.owner_id,
            title=orm.title,
            start_date=orm.start_date,
            end_date=orm.end_date,
            budget=orm.budget,
            status=orm.status,
        )
        t.route_ids = list(orm.route_ids or [])
        t.notes = list(orm.notes or [])
        return t

    @staticmethod
    def _to_orm(trip: Union[Trip, dict]) -> TripORM:
        if isinstance(trip, dict):
            return TripORM(
                id=trip["id"],
                owner_id=trip["owner_id"],
                title=trip["title"],
                start_date=trip["start_date"],
                end_date=trip["end_date"],
                budget=trip["budget"],
                status=trip.get("status", "PLANNED"),
                route_ids=trip.get("route_ids", []),
                notes=trip.get("notes", []),
            )
        return TripORM(
            id=trip.trip_id,
            owner_id=trip.owner_id,
            title=trip.title,
            start_date=trip.start_date,
            end_date=trip.end_date,
            budget=trip.budget,
            status=trip.status,
            route_ids=trip.route_ids,
            notes=trip.notes,
        )

    # ------------------------------------------------------------------ #
    # public interface
    # ------------------------------------------------------------------ #

    def save(self, trip: Union[Trip, dict]) -> None:
        with SessionLocal() as db:
            orm = self._to_orm(trip)
            existing = db.get(TripORM, orm.id)
            if existing:
                existing.owner_id   = orm.owner_id
                existing.title      = orm.title
                existing.start_date = orm.start_date
                existing.end_date   = orm.end_date
                existing.budget     = orm.budget
                existing.status     = orm.status
                existing.route_ids  = orm.route_ids
                existing.notes      = orm.notes
            else:
                db.add(orm)
            db.commit()

    def find_by_id(self, trip_id: str) -> Optional[Trip]:
        with SessionLocal() as db:
            orm = db.get(TripORM, trip_id)
            return self._to_domain(orm) if orm else None

    def find_by_owner(self, owner_id: str) -> List[Trip]:
        with SessionLocal() as db:
            rows = db.query(TripORM).filter(TripORM.owner_id == owner_id).all()
            return [self._to_domain(r) for r in rows]

    def find_active_trips(self) -> List[Trip]:
        with SessionLocal() as db:
            rows = (
                db.query(TripORM)
                .filter(TripORM.status != "COMPLETED")
                .all()
            )
            return [self._to_domain(r) for r in rows]
