from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security import SecurityProfile, SecurityTool


class SecurityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_categories(self) -> Sequence[SecurityProfile]:
        stmt = select(SecurityProfile).order_by(SecurityProfile.sort_order)
        return (await self.session.execute(stmt)).scalars().all()

    async def list_tools(self) -> Sequence[SecurityTool]:
        stmt = (
            select(SecurityTool)
            .options(joinedload(SecurityTool.security_profile))
            .order_by(SecurityTool.sort_order, SecurityTool.name)
        )
        return (await self.session.execute(stmt)).scalars().all()
