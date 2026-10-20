from datetime import date

from sqlalchemy import Date, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Experience(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "experiences"

    company: Mapped[str] = mapped_column(String(150))
    position: Mapped[str] = mapped_column(String(150))
    location: Mapped[str | None] = mapped_column(String(120))
    start_date: Mapped[date] = mapped_column(Date, index=True)
    end_date: Mapped[date | None] = mapped_column(Date)  # NULL = current role
    description: Mapped[str] = mapped_column(Text)
    technologies: Mapped[list[str]] = mapped_column(
        JSON, default=list
    )
    achievements: Mapped[list[str]] = mapped_column(
        JSON, default=list
    )
