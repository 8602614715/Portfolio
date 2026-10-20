from fastapi import APIRouter

from app.api.deps import SecurityServiceDep
from app.schemas.security import SecurityOverview

router = APIRouter(tags=["security"])


@router.get("/security", response_model=SecurityOverview, summary="Cybersecurity overview")
async def get_security(service: SecurityServiceDep) -> SecurityOverview:
    """Focus areas and tools. Purely descriptive: no numeric skill ratings are exposed."""
    return await service.get_overview()
