from datetime import date

from app.schemas.common import ORMModel


class CertificationRead(ORMModel):
    name: str
    issuer: str
    issue_date: date | None
    credential_url: str | None
    description: str | None
