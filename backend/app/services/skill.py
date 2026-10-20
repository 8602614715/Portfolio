from app.models.enums import SkillCategory
from app.repositories.skill import SkillRepository
from app.schemas.skill import SkillGroup

_CATEGORY_ORDER = list(SkillCategory)


class SkillService:
    def __init__(self, repo: SkillRepository) -> None:
        self.repo = repo

    async def list_grouped(self, category: SkillCategory | None = None) -> list[SkillGroup]:
        skills = await self.repo.list(category.value if category else None)
        grouped: dict[SkillCategory, list[str]] = {}
        for skill in skills:
            grouped.setdefault(SkillCategory(skill.category), []).append(skill.name)
        return [
            SkillGroup(category=cat, skills=grouped[cat])
            for cat in _CATEGORY_ORDER
            if cat in grouped
        ]
