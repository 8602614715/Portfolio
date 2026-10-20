from fastapi import APIRouter

from app.api.deps import CertificationServiceDep
from app.schemas.certification import CertificationRead

router = APIRouter(tags=["certifications"])


@router.get(
    "/certifications", response_model=list[CertificationRead], summary="Certifications"
)
async def list_certifications(service: CertificationServiceDep) -> list[CertificationRead]:
    return await service.list_certifications()
