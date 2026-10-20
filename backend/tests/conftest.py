"""Test fixtures.

The suite runs against a REAL PostgreSQL database whose name must end in ``_test``.
At session start it migrates that database from scratch (downgrade -> upgrade) and
seeds it, so the tests also prove the migrations are reproducible.
"""

import asyncio
import os
from collections.abc import AsyncIterator
from pathlib import Path

import httpx
import pytest
from alembic import command
from alembic.config import Config
from dotenv import dotenv_values
from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

ROOT = Path(__file__).resolve().parent.parent


def _resolve_test_database_url() -> str:
    explicit = os.environ.get("TEST_DATABASE_URL") or dotenv_values(ROOT / ".env").get("TEST_DATABASE_URL")
    if explicit:
        return explicit
    base = os.environ.get("DATABASE_URL") or dotenv_values(ROOT / ".env").get("DATABASE_URL")
    if not base:
        pytest.exit("Set DATABASE_URL (or TEST_DATABASE_URL) to run the tests.", returncode=2)
    url = make_url(base)
    return url.set(database=f"{url.database}_test").render_as_string(hide_password=False)


TEST_DATABASE_URL = _resolve_test_database_url()
if not (make_url(TEST_DATABASE_URL).database or "").endswith("_test"):
    pytest.exit("Refusing to run: the test database name must end with '_test'.", returncode=2)

# Must be set before the app (and its cached settings) is imported.
os.environ.update(
    DATABASE_URL=TEST_DATABASE_URL,
    ENVIRONMENT="testing",
    FRONTEND_URL="http://localhost:3000",
)

from app.core.security import get_contact_rate_limiter  # noqa: E402
from app.db.database import dispose_engine  # noqa: E402
from app.db.seed import seed  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


async def _seed_database() -> None:
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with async_sessionmaker(engine, expire_on_commit=False)() as session:
        await seed(session)
    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def database() -> None:
    config = Config(str(ROOT / "alembic.ini"))
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    asyncio.run(_seed_database())
    yield
    command.downgrade(config, "base")


@pytest.fixture(autouse=True)
def _reset_rate_limiter() -> None:
    get_contact_rate_limiter().reset()


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client
    app.dependency_overrides.clear()
    await dispose_engine()  # pooled connections are bound to the per-test event loop


@pytest.fixture
async def db_query():
    """Run a read-only SQL statement against the test DB and return all rows."""

    async def run(sql: str) -> list:
        engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
        async with engine.connect() as conn:
            rows = (await conn.execute(text(sql))).all()
        await engine.dispose()
        return rows

    return run


@pytest.fixture(autouse=True)
async def _clean_contact_messages(db_query):
    yield
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM contact_messages"))
    await engine.dispose()
