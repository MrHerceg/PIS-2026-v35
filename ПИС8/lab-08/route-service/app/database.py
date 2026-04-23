# route-service/app/database.py
import os

from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://poekhali:poekhali@route-db:5432/routes",
)

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class RouteORM(Base):
    __tablename__ = "routes"

    id          = Column(String(36), primary_key=True)
    owner_id    = Column(String(255), nullable=False, index=True)
    title       = Column(String(255), nullable=False)
    origin      = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    start_date  = Column(Date, nullable=False)
    end_date    = Column(Date, nullable=False)
    status      = Column(String(50), nullable=False, default="draft")
    description = Column(String(500), nullable=True)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
