# Satyam Prajapati — Portfolio API

Backend for the interactive cybersecurity portfolio site (the Linux-style terminal UI). It is a **public, read-mostly REST API**: the frontend calls it to render `whoami`, `skills`, `projects`, `security`, and so on, and visitors can leave a message through the contact form.

It only **stores and serves portfolio information**. It contains no scanning, malware-analysis or offensive-security functionality (the "Cyber Fraud Detection System" entry is just a project description).

## 1. Architecture

```
app/
├── main.py            # app factory: middleware, CORS, error handlers, routers
├── api/
│   ├── router.py      # mounts everything under /api/v1
│   ├── deps.py        # dependency injection: session -> repository -> service
│   └── routes/        # thin HTTP layer, no DB logic
├── services/          # business logic (404s, grouping, mapping to schemas)
├── repositories/      # all SQLAlchemy queries
├── models/            # SQLAlchemy 2.x declarative models
├── schemas/           # Pydantic v2 request/response models and validation
├── core/
│   ├── config.py      # settings from environment variables
│   ├── errors.py      # centralised error handling / error format
│   ├── logging.py     # structured JSON logging
│   ├── middleware.py  # body-size limit, request logging, security headers
│   └── security.py    # contact rate limiter, client-IP helper
└── db/
    ├── base.py        # Base + UUID / timestamp mixins
    ├── database.py    # async engine + session dependency
    └── seed.py        # portfolio content (single source of truth)
alembic/               # migrations (0001 = initial schema)
tests/                 # pytest + httpx, run against a real PostgreSQL test DB
```

Request flow: `route -> service -> repository -> database`. Routes never touch the database; services hold the logic; repositories own the queries; schemas validate input and shape output. The stack is async end to end (FastAPI, SQLAlchemy 2 async, psycopg 3). Alembic uses a plain sync engine.

Primary keys are UUIDs everywhere. Content tables have `created_at` / `updated_at`.

## 2. Requirements

- Python 3.12+
- SQLite (default, no separate server required) or PostgreSQL 14+

## 3. Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then edit .env
```

## 4. Database setup

The default `.env` uses a local SQLite database file at `backend/portfolio.db`.
Run the migrations and seed command in sections 6 and 7 to create it. To use
PostgreSQL instead, update `DATABASE_URL` and create the database:

```sql
CREATE USER portfolio WITH PASSWORD 'choose-a-strong-password';
CREATE DATABASE satyam_portfolio OWNER portfolio;
CREATE DATABASE satyam_portfolio_test OWNER portfolio;   -- used by the test suite
```

## 5. Environment variables

| Variable | Required | Default | Notes |
|---|---|---|---|
| `DATABASE_URL` | no | `sqlite+aiosqlite:///./portfolio.db` | Use the default for SQLite, or set `postgresql+psycopg://user:pass@host:5432/db` for PostgreSQL. `postgres://` / `postgresql://` are rewritten to the psycopg 3 driver. |
| `FRONTEND_URL` | no | `http://localhost:3000` | Allowed CORS origin(s), comma-separated. Wildcards are rejected; must be `https://` in production. |
| `ENVIRONMENT` | no | `development` | `development`, `testing` or `production`. Production disables `/docs`, `/redoc`, `/openapi.json` and enables HSTS. |
| `LOG_LEVEL` | no | `INFO` | |
| `MAX_REQUEST_BODY_BYTES` | no | `16384` | Larger bodies get `413`. |
| `CONTACT_RATE_LIMIT_MAX_REQUESTS` | no | `5` | Per client IP, per window. |
| `CONTACT_RATE_LIMIT_WINDOW_SECONDS` | no | `600` | |
| `TRUST_PROXY_HEADERS` | no | `false` | Set `true` only behind exactly one trusted reverse proxy, otherwise the rate limit sees the proxy's IP. |
| `TEST_DATABASE_URL` | no | `DATABASE_URL` + `_test` | The database name **must** end in `_test`. |

`.env` is git-ignored. Never commit it.

## 6. Database migrations

```bash
alembic upgrade head      # create / update the schema
alembic downgrade base    # drop everything (dev only)
```

## 7. Seed data

```bash
python -m app.db.seed
```

The seed content lives in `app/db/seed.py`. Re-running it **replaces** all portfolio content (profile, skills, projects, experience, education, certifications, security data) and **never touches** `contact_messages`.

Several fields are intentionally empty (`TODO` in the file) because they need your real details: public email, GitHub / LinkedIn / resume URLs, project repo links, education dates, and all experience and certification entries. Nothing was invented for these, so `GET /experience` and `GET /certifications` return `[]` until you add entries.

A fresh install is reproducible with: create DB -> `alembic upgrade head` -> `python -m app.db.seed`.

## 8. Running the server

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000/api/v1
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Production example (behind a TLS-terminating proxy):

```bash
ENVIRONMENT=production uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 9. Running tests

```bash
pytest
```

The suite migrates the `*_test` database from scratch (`downgrade base` -> `upgrade head`), seeds it, runs against real PostgreSQL, then downgrades again. It refuses to run against a database whose name does not end in `_test`.

## 10. API endpoints

All under `/api/v1`.

| Method | Path | Description |
|---|---|---|
| GET | `/health` | `{"status": "ok", "environment": ..., "version": ...}` |
| GET | `/profile` | Public profile: name, headline, secondary_title, bio, location, email, github_url, linkedin_url, resume_url |
| GET | `/skills` | Skills grouped by category (`programming`, `backend`, `frontend`, `cybersecurity`, `networking`, `database`, `tools`). Optional `?category=`. |
| GET | `/projects` | Projects, featured first. Optional `?category=cybersecurity\|backend\|frontend\|fullstack\|networking`. |
| GET | `/projects/{project_id}` | One project by UUID. |
| GET | `/experience` | Work experience, most recent first. |
| GET | `/education` | Education history. |
| GET | `/certifications` | Certifications. |
| GET | `/security` | Security focus areas and tools (descriptive, no numeric ratings). |
| POST | `/contact` | Store a contact message. `201` on success. |

Contact request:

```json
{ "name": "Ada Lovelace", "email": "ada@example.com", "message": "Hello!" }
```

Rules: name 2-100 characters (letters from any script, spaces, `-`, `'`, `.`); valid email; message 5-2000 characters after trimming; control characters (except newlines/tabs) are rejected; unknown fields are rejected; 5 requests per 10 minutes per IP.

Errors always look like this (validation errors add a `details` list of `field` + `message`, never the submitted value):

```json
{ "success": false, "error": { "code": "PROJECT_NOT_FOUND", "message": "Project not found" } }
```

| Status | Codes |
|---|---|
| 404 | `PROJECT_NOT_FOUND`, `PROFILE_NOT_FOUND`, `NOT_FOUND` |
| 405 | `METHOD_NOT_ALLOWED` |
| 413 | `PAYLOAD_TOO_LARGE` |
| 422 | `VALIDATION_ERROR` |
| 429 | `RATE_LIMIT_EXCEEDED` (with `Retry-After`) |
| 500 | `INTERNAL_ERROR` |
| 503 | `SERVICE_UNAVAILABLE` (database problems) |

## 11. Security considerations

- **Input validation:** Pydantic v2 on every input; contact payload is strict (`extra="forbid"`), length-limited and control-character-checked. Message text is stored as inert data, so **the frontend must escape it if it ever renders it** (React does by default).
- **SQL injection:** all queries go through SQLAlchemy with bound parameters. No string-built SQL.
- **Safe errors:** one central handler. Responses never contain SQL, stack traces, file paths or credentials; database errors become a generic `503`, unexpected errors a generic `500`. Validation errors do not echo submitted values. The engine uses `hide_parameters=True` so bound values stay out of exceptions and logs.
- **CORS:** explicit origins from `FRONTEND_URL`; no wildcard, no credentials; only `GET`/`POST`/`OPTIONS` and `Content-Type`/`Accept` headers.
- **Request size:** bodies over `MAX_REQUEST_BODY_BYTES` are rejected, including chunked uploads without a `Content-Length`.
- **Rate limiting:** `POST /contact` is limited per client IP. The limiter is in memory and per process, so with N workers the real limit is N times higher; use a shared store or a proxy-level limit if that matters. Behind a reverse proxy, set `TRUST_PROXY_HEADERS=true` (single trusted proxy only).
- **Security headers:** `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`, a locked-down `Content-Security-Policy` (relaxed only for `/docs` and `/redoc`), and HSTS in production.
- **Logging:** structured JSON with request id, method, path, status and duration. Query strings, headers and bodies are never logged, and contact messages are logged by row id only.
- **Secrets:** configuration only through environment variables; `.env` is git-ignored.
- **No authentication:** this is a public, read-only portfolio API plus one rate-limited write endpoint. There is no login/register surface. Contact messages are read directly from the database (`SELECT * FROM contact_messages ORDER BY created_at DESC`); there is deliberately no endpoint that exposes them.
- **Production checklist:** run behind HTTPS, set `ENVIRONMENT=production`, set `FRONTEND_URL` to the real https origin, use a least-privilege database user, and consider a proxy-level rate limit.
