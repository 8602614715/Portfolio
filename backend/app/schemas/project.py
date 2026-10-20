import uuid
from datetime import datetime

from app.models.enums import ProjectCategory
from app.schemas.common import ORMModel


class ProjectRead(ORMModel):
    id: uuid.UUID
    title: str
    slug: str
    short_description: str
    description: str
    category: ProjectCategory
    technologies: list[str]
    features: list[str]
    github_url: str | None
    live_url: str | None
    image_url: str | None
    featured: bool
    created_at: datetime
    updated_at: datetime
