"""Application settings, loaded from environment variables (and .env)."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_NAME = "Satyam Prajapati - Portfolio API"
API_VERSION = "1.0.0"
DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///./portfolio.db"


class Settings(BaseSettings):
    """Runtime configuration. No credentials are ever hardcoded."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = DEFAULT_DATABASE_URL
    frontend_url: str = "http://localhost:3000"
    environment: Literal["development", "testing", "production"] = "development"
    log_level: str = "INFO"

    max_request_body_bytes: int = Field(default=16 * 1024, gt=0)
    contact_rate_limit_max_requests: int = Field(default=5, gt=0)
    contact_rate_limit_window_seconds: int = Field(default=600, gt=0)
    trust_proxy_headers: bool = False

    @field_validator("database_url")
    @classmethod
    def _use_psycopg_driver(cls, value: str) -> str:
        """Normalise supported database URLs for the async application engine."""
        for prefix in ("postgres://", "postgresql://"):
            if value.startswith(prefix):
                return "postgresql+psycopg://" + value[len(prefix):]
        if value.startswith("sqlite:///"):
            return "sqlite+aiosqlite:///" + value.removeprefix("sqlite:///")
        return value

    @field_validator("frontend_url")
    @classmethod
    def _validate_frontend_origins(cls, value: str) -> str:
        origins = [item.strip().rstrip("/") for item in value.split(",") if item.strip()]
        if not origins:
            raise ValueError("FRONTEND_URL must contain at least one origin")
        for origin in origins:
            if not origin.startswith(("http://", "https://")) or "*" in origin:
                raise ValueError(
                    "FRONTEND_URL entries must be explicit http(s) origins; wildcards are not allowed"
                )
        return ",".join(origins)

    @field_validator("log_level")
    @classmethod
    def _normalise_log_level(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def _require_https_in_production(self) -> "Settings":
        if self.environment == "production" and any(
            not origin.startswith("https://") for origin in self.cors_origins
        ):
            raise ValueError("FRONTEND_URL must use https:// when ENVIRONMENT=production")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return self.frontend_url.split(",")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def docs_enabled(self) -> bool:
        return not self.is_production

    @property
    def sync_database_url(self) -> str:
        """Return a driver URL suitable for Alembic's synchronous engine."""
        return self.database_url.replace("sqlite+aiosqlite://", "sqlite://", 1)


@lru_cache
def get_settings() -> Settings:
    return Settings()
