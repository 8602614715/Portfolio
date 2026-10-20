from datetime import date

from app.schemas.common import ORMModel


class EducationRead(ORMModel):
    degree: str
    field: str
    institution: str
    location: str | None
    start_date: date | None
    end_date: date | None
    description: str | None
