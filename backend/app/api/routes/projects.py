import uuid

from fastapi import APIRouter, Query

from app.api.deps import ProjectServiceDep
from app.models.enums import ProjectCategory
from app.schemas.common import ErrorResponse
from app.schemas.project import ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead], summary="List projects")
async def list_projects(
    service: ProjectServiceDep,
    category: ProjectCategory | None = Query(default=None, description="Filter by category"),
) -> list[ProjectRead]:
    """Featured projects first, then newest first."""
    return await service.list_projects(category)


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get one project",
    responses={404: {"model": ErrorResponse, "description": "PROJECT_NOT_FOUND"}},
)
async def get_project(project_id: uuid.UUID, service: ProjectServiceDep) -> ProjectRead:
    return await service.get_project(project_id)
