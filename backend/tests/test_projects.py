import uuid

import pytest

pytestmark = pytest.mark.anyio

PROJECT_FIELDS = {
    "id", "title", "slug", "short_description", "description", "category", "technologies",
    "features", "github_url", "live_url", "image_url", "featured", "created_at", "updated_at",
}


async def test_list_projects(client):
    response = await client.get("/api/v1/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) >= 1
    assert all(set(p) == PROJECT_FIELDS for p in projects)
    assert projects[0]["featured"] is True  # featured first


async def test_main_project_seeded(client):
    projects = (await client.get("/api/v1/projects", params={"category": "cybersecurity"})).json()
    fraud = next(p for p in projects if p["slug"] == "cyber-fraud-detection-system")
    assert fraud["technologies"] == ["FastAPI", "React", "PostgreSQL", "VirusTotal API"]
    assert fraud["features"] == [
        "File scanning", "URL scanning", "Domain scanning", "IP scanning",
        "Email-related security analysis",
    ]


async def test_filter_by_category(client):
    for category in ("cybersecurity", "backend", "frontend", "fullstack", "networking"):
        response = await client.get("/api/v1/projects", params={"category": category})
        assert response.status_code == 200
        assert all(p["category"] == category for p in response.json())


async def test_filter_invalid_category(client):
    response = await client.get("/api/v1/projects", params={"category": "nope"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


async def test_get_project_by_id(client):
    listed = (await client.get("/api/v1/projects")).json()[0]
    response = await client.get(f"/api/v1/projects/{listed['id']}")
    assert response.status_code == 200
    assert response.json() == listed


async def test_get_missing_project(client):
    response = await client.get(f"/api/v1/projects/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "error": {"code": "PROJECT_NOT_FOUND", "message": "Project not found"},
    }


async def test_get_project_malformed_id(client):
    response = await client.get("/api/v1/projects/not-a-uuid")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
