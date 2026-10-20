from app.repositories.security import SecurityRepository
from app.schemas.security import SecurityCategoryRead, SecurityOverview, SecurityToolRead


class SecurityService:
    def __init__(self, repo: SecurityRepository) -> None:
        self.repo = repo

    async def get_overview(self) -> SecurityOverview:
        categories = await self.repo.list_categories()
        tools = await self.repo.list_tools()
        return SecurityOverview(
            categories=[SecurityCategoryRead.model_validate(c) for c in categories],
            tools=[
                SecurityToolRead(
                    name=t.name,
                    description=t.description,
                    category=t.security_profile.category if t.security_profile else None,
                )
                for t in tools
            ],
        )
