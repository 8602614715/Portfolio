from app.schemas.common import ORMModel


class ProfileRead(ORMModel):
    name: str
    headline: str
    secondary_title: str | None
    bio: str
    location: str | None
    email: str | None
    github_url: str | None
    linkedin_url: str | None
    resume_url: str | None
