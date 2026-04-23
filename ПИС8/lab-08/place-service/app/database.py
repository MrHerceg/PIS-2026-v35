# place-service/app/database.py
import os

from sqlalchemy import Column, Date, Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://poekhali:poekhali@place-db:5432/places",
)

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class PlaceORM(Base):
    __tablename__ = "places"

    id         = Column(String(36), primary_key=True)
    route_id   = Column(String(36), nullable=False, index=True)
    name       = Column(String(255), nullable=False)
    latitude   = Column(Float, default=0.0)
    longitude  = Column(Float, default=0.0)
    visit_date = Column(Date, nullable=True)


class BudgetORM(Base):
    __tablename__ = "budgets"

    id       = Column(String(36), primary_key=True)
    route_id = Column(String(36), nullable=False, unique=True, index=True)
    amount   = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="BYN")


class NoteORM(Base):
    __tablename__ = "notes"

    id       = Column(String(36), primary_key=True)
    route_id = Column(String(36), nullable=False, index=True)
    text     = Column(String(2000), nullable=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
