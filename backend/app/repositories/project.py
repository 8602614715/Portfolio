import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, category: str | None = None) -> Sequence[Project]:
        stmt = select(Project).order_by(
            Project.featured.desc(), Project.created_at.desc(), Project.title
        )
        if category is not None:
            stmt = stmt.where(Project.category == category)
        return (await self.session.execute(stmt)).scalars().all()

    async def get(self, project_id: uuid.UUID) -> Project | None:
        return await self.session.get(Project, project_id)
