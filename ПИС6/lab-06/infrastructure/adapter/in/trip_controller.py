from datetime import date
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from application.command.create_trip_command import CreateTripCommand
from application.command.handlers.create_trip_handler import CreateTripHandler
from application.command.add_place_command import AddPlaceToRouteCommand
from application.command.handlers.add_place_handler import AddPlaceToRouteHandler
from application.command.update_budget_command import UpdateBudgetCommand
from application.command.handlers.update_budget_handler import UpdateBudgetHandler
from application.query.get_trip_by_id_query import GetTripByIdQuery
from application.query.handlers.get_trip_by_id_handler import GetTripByIdHandler
from application.query.list_trips_by_owner_query import ListTripsByOwnerQuery
from application.query.handlers.list_trips_by_owner_handler import ListTripsByOwnerHandler
from infrastructure.adapter.out.in_memory_trip_repository import InMemoryTripRepository

app = FastAPI(title="Поехали! API")

# Единственный репозиторий на всё время жизни приложения (для E2E-тестов)
_repo = InMemoryTripRepository()


# ─── Pydantic schemas ─────────────────────────────────────────────────────────

class CreateTripRequest(BaseModel):
    owner_id: str
    title: str
    start_date: date
    end_date: date
    budget: float


class TripResponse(BaseModel):
    id: str
    owner_id: str
    title: str
    start_date: date
    end_date: date
    budget: float
    status: str
    route_ids: List[str] = []
    notes: List[str] = []


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.post("/api/trips", response_model=TripResponse)
def create_trip(body: CreateTripRequest):
    if body.end_date < body.start_date:
        raise HTTPException(status_code=400, detail="end_date must be >= start_date")

    cmd = CreateTripCommand(
        owner_id=body.owner_id,
        title=body.title,
        start_date=body.start_date,
        end_date=body.end_date,
        budget=body.budget,
    )
    handler = CreateTripHandler(_repo)
    trip_id = handler.handle(cmd)

    trip = _repo.find_by_id(trip_id)
    return TripResponse(
        id=trip.id,
        owner_id=trip.owner_id,
        title=trip.title,
        start_date=trip.start_date,
        end_date=trip.end_date,
        budget=trip.budget,
        status=trip.status,
        route_ids=trip.route_ids,
        notes=trip.notes,
    )


@app.get("/api/trips", response_model=List[TripResponse])
def list_trips(owner_id: str):
    handler = ListTripsByOwnerHandler(_repo)
    dtos = handler.handle(ListTripsByOwnerQuery(owner_id=owner_id))
    return [
        TripResponse(
            id=d.id,
            owner_id=d.owner_id,
            title=d.title,
            start_date=d.start_date,
            end_date=d.end_date,
            budget=d.budget,
            status=d.status,
            route_ids=d.route_ids,
            notes=d.notes,
        )
        for d in dtos
    ]


@app.get("/api/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: str):
    handler = GetTripByIdHandler(_repo)
    dto = handler.handle(GetTripByIdQuery(trip_id=trip_id))
    if dto is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripResponse(
        id=dto.id,
        owner_id=dto.owner_id,
        title=dto.title,
        start_date=dto.start_date,
        end_date=dto.end_date,
        budget=dto.budget,
        status=dto.status,
        route_ids=dto.route_ids,
        notes=dto.notes,
    )


@app.post("/api/trips/{trip_id}/add-place")
def add_place(trip_id: str, place_id: str):
    cmd = AddPlaceToRouteCommand(trip_id=trip_id, place_id=place_id)
    try:
        AddPlaceToRouteHandler(_repo).handle(cmd)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"trip_id": trip_id, "place_id": place_id}


@app.patch("/api/trips/{trip_id}/budget")
def update_budget(trip_id: str, budget: float):
    cmd = UpdateBudgetCommand(trip_id=trip_id, budget=budget)
    try:
        UpdateBudgetHandler(_repo).handle(cmd)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    trip = _repo.find_by_id(trip_id)
    return {"trip_id": trip_id, "budget": trip.budget}
