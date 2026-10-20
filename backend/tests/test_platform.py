"""Cross-cutting behaviour: errors, security headers, CORS, size limits, logging, config."""

import logging

import httpx
import pytest
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError

from app.core.config import Settings
from app.db.database import get_session
from app.main import app

pytestmark = pytest.mark.anyio

LEAKY_MARKERS = ("SELECT", "secret_table", "hunter2", "password authentication", "Traceback", "/srv/")


class BrokenSession:
    """Stands in for a session whose database has gone away."""

    @staticmethod
    def _error() -> OperationalError:
        return OperationalError(
            "SELECT * FROM secret_table WHERE token = :t",
            {"t": "hunter2"},
            Exception("password authentication failed for user portfolio"),
        )

    async def execute(self, *_a, **_k):
        raise self._error()

    async def get(self, *_a, **_k):
        raise self._error()

    def add(self, _obj):
        pass

    async def commit(self):
        raise self._error()


def _app_log_text(caplog) -> str:
    """All text the application itself logged (third-party client loggers excluded)."""
    return " ".join(
        f"{r.getMessage()} {vars(r)}" for r in caplog.records if r.name.startswith("app")
    )


def _use_session(session_obj):
    async def override():
        yield session_obj

    app.dependency_overrides[get_session] = override


# ---------------------------------------------------------------- database errors
@pytest.mark.parametrize(
    "path",
    ["profile", "skills", "projects", "experience", "education", "certifications", "security",
     "projects/00000000-0000-0000-0000-000000000001"],
)
async def test_database_error_on_reads_is_safe(client, path):
    _use_session(BrokenSession())
    response = await client.get(f"/api/v1/{path}")
    assert response.status_code == 503
    assert response.json() == {
        "success": False,
        "error": {"code": "SERVICE_UNAVAILABLE", "message": "Service temporarily unavailable"},
    }
    assert not any(marker in response.text for marker in LEAKY_MARKERS)


async def test_database_error_on_contact_is_safe(client):
    _use_session(BrokenSession())
    payload = {"name": "Ada", "email": "ada@example.com", "message": "Hello there friend"}
    response = await client.post("/api/v1/contact", json=payload)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert not any(marker in response.text for marker in LEAKY_MARKERS)


async def test_unexpected_exception_returns_generic_500(client):
    class Exploding:
        async def execute(self, *_a, **_k):
            raise RuntimeError("boom at /srv/app/secret_module.py with hunter2")

    _use_session(Exploding())
    response = await client.get("/api/v1/skills")
    assert response.status_code == 500
    assert response.json() == {
        "success": False,
        "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
    }
    assert not any(marker in response.text for marker in LEAKY_MARKERS)
    assert response.headers["x-content-type-options"] == "nosniff"  # headers survive a 500


async def test_unknown_route_uses_standard_error_shape(client):
    response = await client.get("/api/v1/nothing-here")
    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "error": {"code": "NOT_FOUND", "message": "Resource not found"},
    }


# ---------------------------------------------------------------- headers & docs
async def test_security_headers(client):
    headers = (await client.get("/api/v1/health")).headers
    assert headers["x-content-type-options"] == "nosniff"
    assert headers["x-frame-options"] == "DENY"
    assert headers["referrer-policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in headers["content-security-policy"]
    assert "strict-transport-security" not in headers  # HSTS only in production
    assert headers["x-request-id"]


async def test_docs_available_outside_production(client):
    for path in ("/docs", "/redoc", "/openapi.json"):
        assert (await client.get(path)).status_code == 200


async def test_openapi_documents_every_endpoint(client):
    paths = (await client.get("/openapi.json")).json()["paths"]
    expected = {
        "/api/v1/health", "/api/v1/profile", "/api/v1/skills", "/api/v1/projects",
        "/api/v1/projects/{project_id}", "/api/v1/experience", "/api/v1/education",
        "/api/v1/certifications", "/api/v1/security", "/api/v1/contact",
    }
    assert expected <= set(paths)


async def test_production_disables_docs_and_enables_hsts(monkeypatch):
    import app.main as main

    prod = Settings(
        database_url="postgresql+psycopg://u:p@localhost/x",
        environment="production",
        frontend_url="https://portfolio.example.com",
    )
    monkeypatch.setattr(main, "get_settings", lambda: prod)
    prod_app = main.create_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=prod_app), base_url="http://t") as c:
        assert (await c.get("/docs")).status_code == 404
        assert (await c.get("/openapi.json")).status_code == 404
        health = await c.get("/api/v1/health")
        assert "max-age" in health.headers["strict-transport-security"]


# ---------------------------------------------------------------- CORS
async def test_cors_allows_configured_frontend(client):
    response = await client.get("/api/v1/health", headers={"Origin": "http://localhost:3000"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-credentials" not in response.headers


async def test_cors_preflight_for_contact(client):
    response = await client.options(
        "/api/v1/contact",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "POST" in response.headers["access-control-allow-methods"]


async def test_cors_rejects_other_origins(client):
    response = await client.get("/api/v1/health", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in response.headers
    preflight = await client.options(
        "/api/v1/contact",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert preflight.status_code == 400
    assert "access-control-allow-origin" not in preflight.headers


async def test_cors_is_never_wildcard(client):
    response = await client.get("/api/v1/health", headers={"Origin": "http://localhost:3000"})
    assert response.headers["access-control-allow-origin"] != "*"


# ---------------------------------------------------------------- body size
async def test_oversized_body_rejected_by_content_length(client):
    response = await client.post(
        "/api/v1/contact", content=b"x" * 20_000, headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 413
    assert response.json()["error"]["code"] == "PAYLOAD_TOO_LARGE"


async def test_oversized_chunked_body_rejected(client):
    async def chunks():
        for _ in range(20):
            yield b"x" * 1000

    response = await client.post(
        "/api/v1/contact", content=chunks(), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 413
    assert response.json()["error"]["code"] == "PAYLOAD_TOO_LARGE"


# ---------------------------------------------------------------- logging
async def test_request_logging_fields_and_no_sensitive_data(client, caplog):
    caplog.set_level(logging.INFO)
    message = "my-very-private-message-body"
    await client.post(
        "/api/v1/contact?token=abc123",
        json={"name": "Ada Lovelace", "email": "ada.private@example.com", "message": message},
    )
    records = [r for r in caplog.records if r.name == "app.request"]
    assert records
    record = records[-1]
    assert (record.method, record.path, record.status_code) == ("POST", "/api/v1/contact", 201)
    assert record.duration_ms >= 0
    everything = _app_log_text(caplog)
    for sensitive in (message, "ada.private@example.com", "Ada Lovelace", "abc123"):
        assert sensitive not in everything


async def test_database_error_log_has_no_sql_or_parameters(client, caplog):
    caplog.set_level(logging.INFO)
    _use_session(BrokenSession())
    await client.get("/api/v1/profile")
    everything = _app_log_text(caplog)
    assert "hunter2" not in everything and "secret_table" not in everything


# ---------------------------------------------------------------- configuration
async def test_settings_reject_wildcard_origin():
    with pytest.raises(ValidationError):
        Settings(database_url="postgresql://u:p@h/d", frontend_url="*")
    with pytest.raises(ValidationError):
        Settings(database_url="postgresql://u:p@h/d", frontend_url="https://*.example.com")


async def test_settings_require_https_in_production():
    with pytest.raises(ValidationError):
        Settings(database_url="postgresql://u:p@h/d", environment="production",
                 frontend_url="http://portfolio.example.com")


async def test_settings_normalise_database_url():
    settings = Settings(database_url="postgres://u:p@h/d", frontend_url="http://localhost:3000")
    assert settings.database_url.startswith("postgresql+psycopg://")
