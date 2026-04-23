# place-service/app/main.py
"""
Place & Budget Service — Bounded Context: Управление местами и бюджетом.

Отвечает за:
  - добавление мест в маршрут
  - управление датами посещения
  - расчёт и контроль бюджета
  - добавление заметок к местам

API:
  POST /routes/{route_id}/places   — добавить место    → публикует PlaceAdded
  GET  /routes/{route_id}/places   — список мест маршрута
  POST /routes/{route_id}/budget   — задать/обновить бюджет → публикует BudgetUpdated
  GET  /routes/{route_id}/budget   — получить бюджет
  POST /routes/{route_id}/notes    — добавить заметку  → публикует NoteAdded
  GET  /routes/{route_id}/notes    — список заметок
"""
from contextlib import asynccontextmanager
from datetime import date
from typing import List, Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import BudgetORM, NoteORM, PlaceORM, create_tables, get_db
from app.events import publish_event


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Place & Budget Service — Поехали!",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Schemas ────────────────────────────────────────────────────────────────────

class AddPlaceRequest(BaseModel):
    name:       str   = Field(..., min_length=1)
    latitude:   float = 0.0
    longitude:  float = 0.0
    visit_date: Optional[date] = None


class PlaceResponse(BaseModel):
    id:         str
    route_id:   str
    name:       str
    latitude:   float
    longitude:  float
    visit_date: Optional[date] = None


class SetBudgetRequest(BaseModel):
    amount:   float = Field(..., ge=0)
    currency: str   = Field(default="BYN", min_length=1)


class BudgetResponse(BaseModel):
    id:       str
    route_id: str
    amount:   float
    currency: str


class AddNoteRequest(BaseModel):
    text: str = Field(..., min_length=1)


class NoteResponse(BaseModel):
    id:       str
    route_id: str
    text:     str


# ── Place Endpoints ────────────────────────────────────────────────────────────

@app.post(
    "/routes/{route_id}/places",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_place(route_id: str, body: AddPlaceRequest, db: Session = Depends(get_db)):
    """
    @app.post("/routes/{route_id}/places")
    def add_place()

    Добавляет место в маршрут. Публикует событие PlaceAdded.
    """
    place_id = str(uuid4())
    orm = PlaceORM(
        id=place_id,
        route_id=route_id,
        name=body.name,
        latitude=body.latitude,
        longitude=body.longitude,
        visit_date=body.visit_date,
    )
    db.add(orm)
    db.commit()
    db.refresh(orm)

    publish_event("PlaceAdded", {
        "place_id": place_id,
        "route_id": route_id,
        "name": body.name,
        "latitude": body.latitude,
        "longitude": body.longitude,
    })

    return PlaceResponse(
        id=orm.id, route_id=orm.route_id, name=orm.name,
        latitude=orm.latitude, longitude=orm.longitude, visit_date=orm.visit_date,
    )


@app.get("/routes/{route_id}/places", response_model=List[PlaceResponse])
def get_places(route_id: str, db: Session = Depends(get_db)):
    """
    @app.get("/routes/{route_id}/places")
    def get_places()

    Возвращает список мест маршрута.
    """
    rows = db.query(PlaceORM).filter(PlaceORM.route_id == route_id).all()
    return [
        PlaceResponse(
            id=r.id, route_id=r.route_id, name=r.name,
            latitude=r.latitude, longitude=r.longitude, visit_date=r.visit_date,
        )
        for r in rows
    ]


# ── Budget Endpoints ───────────────────────────────────────────────────────────

@app.post(
    "/routes/{route_id}/budget",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def set_budget(route_id: str, body: SetBudgetRequest, db: Session = Depends(get_db)):
    """
    @app.post("/routes/{route_id}/budget")
    def set_budget()

    Создаёт или обновляет бюджет маршрута. Публикует событие BudgetUpdated.
    """
    existing = db.query(BudgetORM).filter(BudgetORM.route_id == route_id).first()
    if existing:
        existing.amount   = body.amount
        existing.currency = body.currency
        db.commit()
        db.refresh(existing)
        orm = existing
    else:
        budget_id = str(uuid4())
        orm = BudgetORM(
            id=budget_id,
            route_id=route_id,
            amount=body.amount,
            currency=body.currency,
        )
        db.add(orm)
        db.commit()
        db.refresh(orm)

    publish_event("BudgetUpdated", {
        "route_id": route_id,
        "amount": body.amount,
        "currency": body.currency,
    })

    return BudgetResponse(
        id=orm.id, route_id=orm.route_id,
        amount=orm.amount, currency=orm.currency,
    )


@app.get("/routes/{route_id}/budget", response_model=BudgetResponse)
def get_budget(route_id: str, db: Session = Depends(get_db)):
    """Возвращает бюджет маршрута."""
    orm = db.query(BudgetORM).filter(BudgetORM.route_id == route_id).first()
    if orm is None:
        raise HTTPException(status_code=404, detail="Бюджет не задан")
    return BudgetResponse(
        id=orm.id, route_id=orm.route_id,
        amount=orm.amount, currency=orm.currency,
    )


# ── Note Endpoints ─────────────────────────────────────────────────────────────

@app.post(
    "/routes/{route_id}/notes",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_note(route_id: str, body: AddNoteRequest, db: Session = Depends(get_db)):
    """
    @app.post("/routes/{route_id}/notes")
    def add_note()

    Добавляет заметку к маршруту. Публикует событие NoteAdded.
    """
    note_id = str(uuid4())
    orm = NoteORM(id=note_id, route_id=route_id, text=body.text)
    db.add(orm)
    db.commit()
    db.refresh(orm)

    publish_event("NoteAdded", {
        "note_id": note_id,
        "route_id": route_id,
        "text": body.text,
    })

    return NoteResponse(id=orm.id, route_id=orm.route_id, text=orm.text)


@app.get("/routes/{route_id}/notes", response_model=List[NoteResponse])
def get_notes(route_id: str, db: Session = Depends(get_db)):
    """Возвращает список заметок маршрута."""
    rows = db.query(NoteORM).filter(NoteORM.route_id == route_id).all()
    return [NoteResponse(id=r.id, route_id=r.route_id, text=r.text) for r in rows]


@app.get("/health")
def health():
    return {"service": "place-service", "status": "ok"}
