# infrastructure/config/database.py
"""
Настройка подключения к PostgreSQL через SQLAlchemy.
ORM-модели (таблицы) определены здесь же, чтобы избежать циклических импортов.
"""
import os

from sqlalchemy import (
    Column, Date, Float, ForeignKey, String, Text, create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, relationship, sessionmaker

# ── Connection URL ──────────────────────────────────────────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://poekhali:poekhali@localhost:5432/poekhali",
)

# Allow SQLite for tests (connect_args only needed for sqlite)
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=_connect_args)
SessionLocal: sessionmaker = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# ── Base class ───────────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── ORM Models ───────────────────────────────────────────────────────────────

class TripORM(Base):
    __tablename__ = "trips"

    id          = Column(String(36), primary_key=True)
    owner_id    = Column(String(255), nullable=False, index=True)
    title       = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date  = Column(Date, nullable=False)
    end_date    = Column(Date, nullable=False)
    budget      = Column(Float, nullable=False)
    status      = Column(String(50), nullable=False, default="draft")

    places = relationship("PlaceORM", back_populates="trip", cascade="all, delete-orphan")
    notes  = relationship("NoteORM",  back_populates="trip", cascade="all, delete-orphan")


class PlaceORM(Base):
    __tablename__ = "places"

    id        = Column(String(36), primary_key=True)
    trip_id   = Column(String(36), ForeignKey("trips.id"), nullable=False)
    name      = Column(String(255), nullable=False)
    latitude  = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)

    trip = relationship("TripORM", back_populates="places")


class NoteORM(Base):
    __tablename__ = "notes"

    id      = Column(String(36), primary_key=True)
    trip_id = Column(String(36), ForeignKey("trips.id"), nullable=False)
    text    = Column(Text, nullable=False)

    trip = relationship("TripORM", back_populates="notes")


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_db():
    """FastAPI dependency: yields a SQLAlchemy session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create all tables (used in tests and app startup)."""
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """Drop all tables (used in tests)."""
    Base.metadata.drop_all(bind=engine)
