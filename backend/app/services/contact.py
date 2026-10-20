import logging

from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactRequest, ContactResponse

logger = logging.getLogger("app.contact")


class ContactService:
    def __init__(self, repo: ContactRepository) -> None:
        self.repo = repo

    async def submit(self, data: ContactRequest) -> ContactResponse:
        record = await self.repo.add(data.name, str(data.email), data.message)
        # Log the record id only: never the visitor's name, email or message.
        logger.info("contact message stored", extra={"message_id": str(record.id)})
        return ContactResponse()
