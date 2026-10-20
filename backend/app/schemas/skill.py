from pydantic import BaseModel, Field

from app.models.enums import SkillCategory


class SkillGroup(BaseModel):
    category: SkillCategory
    skills: list[str] = Field(examples=[["Linux", "Nmap", "Burp Suite"]])
