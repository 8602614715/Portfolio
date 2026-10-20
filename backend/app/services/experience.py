from app.repositories.experience import ExperienceRepository
from app.schemas.experience import ExperienceRead


class ExperienceService:
    def __init__(self, repo: ExperienceRepository) -> None:
        self.repo = repo

    async def list_experience(self) -> list[ExperienceRead]:
        return [ExperienceRead.model_validate(e) for e in await self.repo.list()]
