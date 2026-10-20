from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile


class ProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self) -> Profile | None:
        result = await self.session.execute(select(Profile).order_by(Profile.created_at).limit(1))
        return result.scalar_one_or_none()
