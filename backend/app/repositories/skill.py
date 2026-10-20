from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill


class SkillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, category: str | None = None) -> Sequence[Skill]:
        stmt = select(Skill).order_by(Skill.category, Skill.sort_order, Skill.name)
        if category is not None:
            stmt = stmt.where(Skill.category == category)
        return (await self.session.execute(stmt)).scalars().all()
