"""Import every model so Base.metadata (and Alembic) sees all tables."""

from app.models.certification import Certification
from app.models.contact import ContactMessage
from app.models.education import Education
from app.models.experience import Experience
from app.models.profile import Profile
from app.models.project import Project, ProjectTechnology
from app.models.security import SecurityProfile, SecurityTool
from app.models.skill import Skill

__all__ = [
    "Certification",
    "ContactMessage",
    "Education",
    "Experience",
    "Profile",
    "Project",
    "ProjectTechnology",
    "SecurityProfile",
    "SecurityTool",
    "Skill",
]
