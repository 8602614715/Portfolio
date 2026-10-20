from app.repositories.education import EducationRepository
from app.schemas.education import EducationRead


class EducationService:
    def __init__(self, repo: EducationRepository) -> None:
        self.repo = repo

    async def list_education(self) -> list[EducationRead]:
        return [EducationRead.model_validate(e) for e in await self.repo.list()]
