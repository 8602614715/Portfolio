import pytest

pytestmark = pytest.mark.anyio


async def test_skills_grouped(client):
    response = await client.get("/api/v1/skills")
    assert response.status_code == 200
    groups = response.json()
    assert groups and all(set(g) == {"category", "skills"} for g in groups)
    by_category = {g["category"]: g["skills"] for g in groups}
    assert {"Linux", "Nmap", "Burp Suite", "OWASP", "VirusTotal API"} <= set(by_category["cybersecurity"])
    # fixed category order, no empty groups
    order = ["programming", "backend", "frontend", "cybersecurity", "networking", "database", "tools"]
    assert [g["category"] for g in groups] == [c for c in order if c in by_category]
    assert all(g["skills"] for g in groups)


async def test_skills_filter_by_category(client):
    response = await client.get("/api/v1/skills", params={"category": "database"})
    assert response.status_code == 200
    assert [g["category"] for g in response.json()] == ["database"]


async def test_skills_invalid_category(client):
    response = await client.get("/api/v1/skills", params={"category": "witchcraft"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
