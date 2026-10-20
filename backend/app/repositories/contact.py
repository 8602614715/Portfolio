from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactMessage


class ContactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, name: str, email: str, message: str) -> ContactMessage:
        record = ContactMessage(name=name, email=email, message=message)
        self.session.add(record)
        await self.session.commit()
        return record
