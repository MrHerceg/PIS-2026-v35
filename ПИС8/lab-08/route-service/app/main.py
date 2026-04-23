# route-service/app/main.py
"""
Route Service — Bounded Context: Управление маршрутами.

Отвечает за:
  - создание маршрута поездки
  - получение информации о маршруте

API:
  POST /routes         — создать маршрут   → публикует RouteCreated
  GET  /routes/{id}    — получить маршрут
  GET  /routes         — список маршрутов владельца
"""
from contextlib import asynccontextmanager
from datetime import date
from typing import List, Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.database import RouteORM, create_tables, get_db
from app.events import publish_event


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Route Service — Поехали!", version="1.0.0", lifespan=lifespan)


# ── Schemas ────────────────────────────────────────────────────────────────────

class CreateRouteRequest(BaseModel):
    owner_id:    str  = Field(..., min_length=1)
    title:       str  = Field(..., min_length=1)
    origin:      str  = Field(..., min_length=1)
    destination: str  = Field(..., min_length=1)
    start_date:  date
    end_date:    date
    description: Optional[str] = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v: date, info) -> date:
        start = info.data.get("start_date")
        if start and v <= start:
            raise ValueError("end_date должна быть позже start_date")
        return v


class RouteResponse(BaseModel):
    id:          str
    owner_id:    str
    title:       str
    origin:      str
    destination: str
    start_date:  date
    end_date:    date
    status:      str
    description: Optional[str] = None


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.post("/routes", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route(body: CreateRouteRequest, db: Session = Depends(get_db)):
    """
    @app.post("/routes")
    def create_route()

    Создаёт новый маршрут поездки.
    Публикует событие RouteCreated в RabbitMQ.
    """
    route_id = str(uuid4())
    orm = RouteORM(
        id=route_id,
        owner_id=body.owner_id,
        title=body.title,
        origin=body.origin,
        destination=body.destination,
        start_date=body.start_date,
        end_date=body.end_date,
        status="draft",
        description=body.description,
    )
    db.add(orm)
    db.commit()
    db.refresh(orm)

    # Publish event to RabbitMQ
    publish_event("RouteCreated", {
        "route_id": route_id,
        "owner_id": body.owner_id,
        "title": body.title,
        "origin": body.origin,
        "destination": body.destination,
    })

    return RouteResponse(
        id=orm.id,
        owner_id=orm.owner_id,
        title=orm.title,
        origin=orm.origin,
        destination=orm.destination,
        start_date=orm.start_date,
        end_date=orm.end_date,
        status=orm.status,
        description=orm.description,
    )


@app.get("/routes/{route_id}", response_model=RouteResponse)
def get_route(route_id: str, db: Session = Depends(get_db)):
    """
    @app.get("/routes/{id}")
    def get_route()

    Возвращает информацию о маршруте по его ID.
    """
    orm = db.get(RouteORM, route_id)
    if orm is None:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return RouteResponse(
        id=orm.id,
        owner_id=orm.owner_id,
        title=orm.title,
        origin=orm.origin,
        destination=orm.destination,
        start_date=orm.start_date,
        end_date=orm.end_date,
        status=orm.status,
        description=orm.description,
    )


@app.get("/routes", response_model=List[RouteResponse])
def list_routes(owner_id: str, db: Session = Depends(get_db)):
    """Список маршрутов по владельцу."""
    rows = db.query(RouteORM).filter(RouteORM.owner_id == owner_id).all()
    return [
        RouteResponse(
            id=r.id, owner_id=r.owner_id, title=r.title,
            origin=r.origin, destination=r.destination,
            start_date=r.start_date, end_date=r.end_date,
            status=r.status, description=r.description,
        )
        for r in rows
    ]


@app.get("/health")
def health():
    return {"service": "route-service", "status": "ok"}
