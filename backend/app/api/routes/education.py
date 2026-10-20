from fastapi import APIRouter

from app.api.deps import EducationServiceDep
from app.schemas.education import EducationRead

router = APIRouter(tags=["education"])


@router.get("/education", response_model=list[EducationRead], summary="Education history")
async def list_education(service: EducationServiceDep) -> list[EducationRead]:
    return await service.list_education()
