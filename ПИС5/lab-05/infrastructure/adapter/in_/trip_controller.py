# infrastructure/adapter/in/trip_controller.py
"""
Входящий адаптер: FastAPI REST-контроллер для поездок.

Эндпоинты:
    POST   /api/trips                  — создать поездку
    GET    /api/trips/{trip_id}        — получить поездку по ID
    GET    /api/trips                  — список поездок владельца
    POST   /api/trips/{trip_id}/places — добавить место в маршрут
    POST   /api/trips/{trip_id}/notes  — добавить заметку
    GET    /api/trips/active           — список активных поездок
"""
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from application.ports import EventPublisher
from application.service.trip_service import TripService
from infrastructure.adapter.out.notification_service import EventNotificationService
from infrastructure.adapter.out.rabbitmq_event_publisher import RabbitMQEventPublisher
from infrastructure.adapter.out.trip_repository import SqlAlchemyTripRepository
from infrastructure.config.database import get_db

router = APIRouter(prefix="/api/trips", tags=["trips"])


# ── Dependency factory ────────────────────────────────────────────────────────

def get_service(db: Session = Depends(get_db)) -> TripService:
    repo = SqlAlchemyTripRepository(db)
    publisher: EventPublisher = RabbitMQEventPublisher()
    notifier = EventNotificationService(publisher)
    return TripService(
        repository=repo,
        geo_service=None,       # подключить StubGeoService или реальный
        notification_service=notifier,
    )


# ── Request / Response schemas ────────────────────────────────────────────────

class CreateTripRequest(BaseModel):
    owner_id:   str   = Field(..., min_length=1)
    title:      str   = Field(..., min_length=1)
    start_date: date
    end_date:   date
    budget:     float = Field(..., ge=0)
    description: Optional[str] = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v: date, info) -> date:
        start = info.data.get("start_date")
        if start and v <= start:
            raise ValueError("end_date должна быть позже start_date")
        return v


class AddPlaceRequest(BaseModel):
    place_id: str = Field(..., min_length=1)


class AddNoteRequest(BaseModel):
    text: str = Field(..., min_length=1)


class TripResponse(BaseModel):
    id:          str
    owner_id:    str
    title:       str
    start_date:  date
    end_date:    date
    budget:      float
    status:      str
    route_ids:   List[str]
    notes:       List[str]
    description: Optional[str] = None

    model_config = {"from_attributes": True}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_trip(
    body: CreateTripRequest,
    svc: TripService = Depends(get_service),
):
    """POST /api/trips — создать новую поездку."""
    trip_id = svc.create_trip(
        owner_id=body.owner_id,
        title=body.title,
        start_date=body.start_date,
        end_date=body.end_date,
        budget=body.budget,
    )
    return {"id": trip_id, "status": "created"}


@router.get("/active", response_model=List[TripResponse])
def list_active_trips(svc: TripService = Depends(get_service)):
    """GET /api/trips/active — список всех активных поездок."""
    trips = svc.list_active_trips()
    return [
        TripResponse(
            id=t.id, owner_id=t.owner_id, title=t.title,
            start_date=t.start_date, end_date=t.end_date,
            budget=t.budget, status=t.status,
            route_ids=t.route_ids, notes=t.notes,
        )
        for t in trips
    ]


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: str, svc: TripService = Depends(get_service)):
    """GET /api/trips/{trip_id} — получить поездку по ID."""
    dto = svc.get_trip_by_id(trip_id)
    if dto is None:
        raise HTTPException(status_code=404, detail="Поездка не найдена")
    return TripResponse(
        id=dto.id, owner_id=dto.owner_id, title=dto.title,
        start_date=dto.start_date, end_date=dto.end_date,
        budget=dto.budget, status=dto.status,
        route_ids=dto.route_ids, notes=dto.notes,
    )


@router.get("", response_model=List[TripResponse])
def list_trips(
    owner_id: str,
    status_filter: Optional[str] = None,
    svc: TripService = Depends(get_service),
):
    """GET /api/trips?owner_id=... — список поездок владельца."""
    trips = svc.list_trips_by_owner(owner_id=owner_id, status=status_filter)
    return [
        TripResponse(
            id=t.id, owner_id=t.owner_id, title=t.title,
            start_date=t.start_date, end_date=t.end_date,
            budget=t.budget, status=t.status,
            route_ids=t.route_ids, notes=t.notes,
        )
        for t in trips
    ]


@router.post("/{trip_id}/places", response_model=dict)
def add_place(
    trip_id: str,
    body: AddPlaceRequest,
    svc: TripService = Depends(get_service),
):
    """POST /api/trips/{trip_id}/places — добавить место в маршрут."""
    try:
        svc.add_place_to_route(trip_id=trip_id, place_id=body.place_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"status": "place added"}


@router.post("/{trip_id}/notes", response_model=dict)
def add_note(
    trip_id: str,
    body: AddNoteRequest,
    svc: TripService = Depends(get_service),
):
    """POST /api/trips/{trip_id}/notes — добавить заметку к поездке."""
    try:
        note_id = svc.add_note(trip_id=trip_id, text=body.text)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"id": note_id, "status": "note added"}
