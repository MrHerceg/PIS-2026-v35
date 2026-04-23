# main.py
"""
Точка входа FastAPI-приложения.

Запуск:
    uvicorn main:app --reload

Swagger UI:
    http://localhost:8000/docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.adapter.in_.trip_controller import router as trip_router
from infrastructure.config.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создать таблицы при старте (для разработки и тестов)
    create_tables()
    yield


app = FastAPI(
    title="Поездки «Поехали!»",
    description="Планы, которые сбываются. REST API для управления поездками.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(trip_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "poekhali-trips"}
