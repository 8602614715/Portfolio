import uuid

from sqlalchemy import ForeignKey, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class SecurityProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """One cybersecurity focus area (e.g. Web Security) with qualitative detail."""

    __tablename__ = "security_profiles"

    category: Mapped[str] = mapped_column(String(80), unique=True)
    description: Mapped[str] = mapped_column(Text)
    focus_areas: Mapped[list[str]] = mapped_column(
        JSON, default=list
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    tools: Mapped[list["SecurityTool"]] = relationship(
        back_populates="security_profile", order_by="SecurityTool.sort_order"
    )


class SecurityTool(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "security_tools"

    name: Mapped[str] = mapped_column(String(80), unique=True)
    description: Mapped[str] = mapped_column(Text)
    security_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("security_profiles.id", ondelete="SET NULL"),
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    security_profile: Mapped[SecurityProfile | None] = relationship(back_populates="tools")
