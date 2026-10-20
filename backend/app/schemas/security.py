from pydantic import BaseModel

from app.schemas.common import ORMModel


class SecurityCategoryRead(ORMModel):
    category: str
    description: str
    focus_areas: list[str]


class SecurityToolRead(BaseModel):
    name: str
    description: str
    category: str | None


class SecurityOverview(BaseModel):
    """Qualitative overview. Deliberately has no numeric 'skill level' fields."""

    categories: list[SecurityCategoryRead]
    tools: list[SecurityToolRead]
