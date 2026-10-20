from datetime import date

from app.schemas.common import ORMModel


class ExperienceRead(ORMModel):
    company: str
    position: str
    location: str | None
    start_date: date
    end_date: date | None
    description: str
    technologies: list[str]
    achievements: list[str]
