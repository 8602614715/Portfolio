from fastapi import APIRouter, Query

from app.api.deps import SkillServiceDep
from app.models.enums import SkillCategory
from app.schemas.skill import SkillGroup

router = APIRouter(tags=["skills"])


@router.get("/skills", response_model=list[SkillGroup], summary="Skills grouped by category")
async def list_skills(
    service: SkillServiceDep,
    category: SkillCategory | None = Query(default=None, description="Return only this category"),
) -> list[SkillGroup]:
    """Skills grouped by category, in a fixed category order. Empty categories are omitted."""
    return await service.list_grouped(category)
