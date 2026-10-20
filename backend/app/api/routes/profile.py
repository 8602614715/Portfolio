from fastapi import APIRouter

from app.api.deps import ProfileServiceDep
from app.schemas.common import ErrorResponse
from app.schemas.profile import ProfileRead

router = APIRouter(tags=["profile"])


@router.get(
    "/profile",
    response_model=ProfileRead,
    summary="Public profile",
    responses={404: {"model": ErrorResponse, "description": "Profile not seeded"}},
)
async def get_profile(service: ProfileServiceDep) -> ProfileRead:
    """Name, headline, bio and public links. No private data is stored or returned."""
    return await service.get_profile()
