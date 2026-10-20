from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import API_VERSION, get_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str


@router.get("/health", response_model=HealthResponse, summary="Liveness check")
async def health() -> HealthResponse:
    """Returns ``ok`` when the API process is up. Does not touch the database."""
    return HealthResponse(
        status="ok", environment=get_settings().environment, version=API_VERSION
    )
