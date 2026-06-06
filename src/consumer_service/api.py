from __future__ import annotations

import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from consumer_service.core_adapter import implementation, moving_average

app = FastAPI(title="Python Consumer Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# record start time for uptime/readiness
start_time = time.time()


class ScoreRequest(BaseModel):
    values: list[float] = Field(..., min_length=1)
    window: int = Field(3, ge=1)


class ScoreResponse(BaseModel):
    moving_average: list[float]
    implementation: str


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "Python Consumer Service",
        "health": "/health",
        "score": "/score",
    }


@app.get("/health")
def health() -> dict[str, object]:
    """General health endpoint including implementation info and uptime."""
    uptime = int(time.time() - start_time)
    return {"status": "ok", "implementation": implementation(), "uptime_seconds": uptime}


@app.get("/ready")
def ready() -> dict[str, object]:
    """Readiness endpoint — simple checks for dependencies can be added here."""
    uptime = int(time.time() - start_time)
    return {"status": "ready", "uptime_seconds": uptime}


@app.get("/version")
def version() -> dict[str, str]:
    return {"service": "Python Consumer Service", "version": app.version}


@app.post("/score", response_model=ScoreResponse)
def score(request: ScoreRequest) -> ScoreResponse:
    return ScoreResponse(
        moving_average=moving_average(request.values, request.window),
        implementation=implementation(),
    )
