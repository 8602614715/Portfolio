from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.experience import Experience


class ExperienceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> Sequence[Experience]:
        stmt = select(Experience).order_by(Experience.start_date.desc())
        return (await self.session.execute(stmt)).scalars().all()
