from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Certification(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "certifications"

    name: Mapped[str] = mapped_column(String(200))
    issuer: Mapped[str] = mapped_column(String(150))
    issue_date: Mapped[date | None] = mapped_column(Date, index=True)
    credential_url: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
