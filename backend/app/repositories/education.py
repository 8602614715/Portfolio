from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.education import Education


class EducationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> Sequence[Education]:
        stmt = select(Education).order_by(Education.start_date.desc().nulls_last())
        return (await self.session.execute(stmt)).scalars().all()
