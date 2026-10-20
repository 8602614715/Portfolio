"""Shared enumerations. Stored as short strings guarded by CHECK constraints."""

from enum import StrEnum


class ProjectCategory(StrEnum):
    CYBERSECURITY = "cybersecurity"
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    NETWORKING = "networking"


class SkillCategory(StrEnum):
    PROGRAMMING = "programming"
    BACKEND = "backend"
    FRONTEND = "frontend"
    CYBERSECURITY = "cybersecurity"
    NETWORKING = "networking"
    DATABASE = "database"
    TOOLS = "tools"


def sql_in(enum_cls: type[StrEnum]) -> str:
    """Render ``'a', 'b'`` for use inside a CHECK ... IN (...) clause."""
    return ", ".join(f"'{member.value}'" for member in enum_cls)
