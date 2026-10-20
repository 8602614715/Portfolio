from app.repositories.certification import CertificationRepository
from app.schemas.certification import CertificationRead


class CertificationService:
    def __init__(self, repo: CertificationRepository) -> None:
        self.repo = repo

    async def list_certifications(self) -> list[CertificationRead]:
        return [CertificationRead.model_validate(c) for c in await self.repo.list()]
