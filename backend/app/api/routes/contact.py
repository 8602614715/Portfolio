from fastapi import APIRouter, Depends, status

from app.api.deps import ContactServiceDep
from app.core.security import contact_rate_limit
from app.schemas.common import ErrorResponse
from app.schemas.contact import ContactRequest, ContactResponse

router = APIRouter(tags=["contact"])


@router.post(
    "/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a message",
    dependencies=[Depends(contact_rate_limit)],
    responses={
        413: {"model": ErrorResponse, "description": "Body too large"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        503: {"model": ErrorResponse, "description": "Storage unavailable"},
    },
)
async def send_message(payload: ContactRequest, service: ContactServiceDep) -> ContactResponse:
    """Validates and stores a contact message. Rate limited per client IP."""
    return await service.submit(payload)
