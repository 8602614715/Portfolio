"""Dependency-injection wiring: session -> repository -> service."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.repositories.certification import CertificationRepository
from app.repositories.contact import ContactRepository
from app.repositories.education import EducationRepository
from app.repositories.experience import ExperienceRepository
from app.repositories.profile import ProfileRepository
from app.repositories.project import ProjectRepository
from app.repositories.security import SecurityRepository
from app.repositories.skill import SkillRepository
from app.services.certification import CertificationService
from app.services.contact import ContactService
from app.services.education import EducationService
from app.services.experience import ExperienceService
from app.services.profile import ProfileService
from app.services.project import ProjectService
from app.services.security import SecurityService
from app.services.skill import SkillService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_profile_service(session: SessionDep) -> ProfileService:
    return ProfileService(ProfileRepository(session))


def get_skill_service(session: SessionDep) -> SkillService:
    return SkillService(SkillRepository(session))


def get_project_service(session: SessionDep) -> ProjectService:
    return ProjectService(ProjectRepository(session))


def get_experience_service(session: SessionDep) -> ExperienceService:
    return ExperienceService(ExperienceRepository(session))


def get_education_service(session: SessionDep) -> EducationService:
    return EducationService(EducationRepository(session))


def get_certification_service(session: SessionDep) -> CertificationService:
    return CertificationService(CertificationRepository(session))


def get_security_service(session: SessionDep) -> SecurityService:
    return SecurityService(SecurityRepository(session))


def get_contact_service(session: SessionDep) -> ContactService:
    return ContactService(ContactRepository(session))


ProfileServiceDep = Annotated[ProfileService, Depends(get_profile_service)]
SkillServiceDep = Annotated[SkillService, Depends(get_skill_service)]
ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
ExperienceServiceDep = Annotated[ExperienceService, Depends(get_experience_service)]
EducationServiceDep = Annotated[EducationService, Depends(get_education_service)]
CertificationServiceDep = Annotated[CertificationService, Depends(get_certification_service)]
SecurityServiceDep = Annotated[SecurityService, Depends(get_security_service)]
ContactServiceDep = Annotated[ContactService, Depends(get_contact_service)]
