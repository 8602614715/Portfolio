from fastapi import APIRouter

from app.api.routes import (
    certifications,
    contact,
    education,
    experience,
    health,
    profile,
    projects,
    security,
    skills,
)

api_router = APIRouter(prefix="/api/v1")
for module in (
    health, profile, skills, projects, experience, education, certifications, security, contact
):
    api_router.include_router(module.router)
