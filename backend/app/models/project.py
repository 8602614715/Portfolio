import uuid

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ProjectCategory, sql_in


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint(f"category IN ({sql_in(ProjectCategory)})", name="category_valid"),
    )

    title: Mapped[str] = mapped_column(String(150))
    slug: Mapped[str] = mapped_column(String(150), unique=True)
    short_description: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(30), index=True)
    features: Mapped[list[str]] = mapped_column(
        JSON, default=list
    )
    github_url: Mapped[str | None] = mapped_column(String(500))
    live_url: Mapped[str | None] = mapped_column(String(500))
    image_url: Mapped[str | None] = mapped_column(String(500))
    featured: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", index=True
    )

    technologies: Mapped[list["ProjectTechnology"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProjectTechnology.sort_order",
        lazy="selectin",
    )


class ProjectTechnology(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "project_technologies"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    project: Mapped[Project] = relationship(back_populates="technologies")
