from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.certification import Certification


class CertificationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> Sequence[Certification]:
        stmt = select(Certification).order_by(Certification.issue_date.desc().nulls_last())
        return (await self.session.execute(stmt)).scalars().all()
