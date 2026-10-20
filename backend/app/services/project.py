import uuid

from app.core.errors import ProjectNotFoundError
from app.models.enums import ProjectCategory
from app.models.project import Project
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectRead


def _to_schema(project: Project) -> ProjectRead:
    return ProjectRead(
        id=project.id,
        title=project.title,
        slug=project.slug,
        short_description=project.short_description,
        description=project.description,
        category=ProjectCategory(project.category),
        technologies=[t.name for t in project.technologies],
        features=list(project.features),
        github_url=project.github_url,
        live_url=project.live_url,
        image_url=project.image_url,
        featured=project.featured,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


class ProjectService:
    def __init__(self, repo: ProjectRepository) -> None:
        self.repo = repo

    async def list_projects(self, category: ProjectCategory | None = None) -> list[ProjectRead]:
        projects = await self.repo.list(category.value if category else None)
        return [_to_schema(p) for p in projects]

    async def get_project(self, project_id: uuid.UUID) -> ProjectRead:
        project = await self.repo.get(project_id)
        if project is None:
            raise ProjectNotFoundError()
        return _to_schema(project)
