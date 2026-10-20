from fastapi import APIRouter

from app.api.deps import ExperienceServiceDep
from app.schemas.experience import ExperienceRead

router = APIRouter(tags=["experience"])


@router.get("/experience", response_model=list[ExperienceRead], summary="Work experience")
async def list_experience(service: ExperienceServiceDep) -> list[ExperienceRead]:
    """Most recent first. ``end_date`` is null for a current role."""
    return await service.list_experience()
