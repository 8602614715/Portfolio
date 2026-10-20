from app.core.errors import ProfileNotFoundError
from app.repositories.profile import ProfileRepository
from app.schemas.profile import ProfileRead


class ProfileService:
    def __init__(self, repo: ProfileRepository) -> None:
        self.repo = repo

    async def get_profile(self) -> ProfileRead:
        profile = await self.repo.get()
        if profile is None:
            raise ProfileNotFoundError()
        return ProfileRead.model_validate(profile)
